import logging
from flask import Flask, render_template, render_template, request, redirect, session,redirect, url_for,jsonify,flash
import os
import mysql.connector
from werkzeug.utils import secure_filename




app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Function to establish database connection
def get_database_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_voiture"
    )
    return connection
# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        # Check if email already exists in the database
        if check_email_exist(email):
            return 'Email already exists. Please choose a different one or login.'
        # Insert new user into the database
        insert_user(nom, prenom, email, mot_de_passe)
        return render_template('index.html')

# Function to get client information by email from the database
def get_client_by_email(email):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Client WHERE email = %s"
        cursor.execute(query, (email,))
        client = cursor.fetchone()
        connection.close()
        return client
    except Exception as e:
        logging.error("Error fetching client by email: %s", str(e))
        return None


# Function to check if email already exists in the database
def check_email_exist(email):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM Client WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    connection.close()
    if user:
        return True
    else:
        return False

# Function to insert new user into the database
def insert_user(nom, prenom, email, mot_de_passe):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "INSERT INTO Client (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nom, prenom, email, mot_de_passe))
    connection.commit()
    connection.close()




# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Assuming you have a function to authenticate the user
        user_type = authenticate_user(email, password)
        if user_type:
            # Storing user email in the session
            session['email'] = email

            # Storing client information in the session if the user is a client
            if user_type == 'client':
                client = get_client_by_email(email)
                session['client'] = client

            # Redirect to the appropriate route based on user type
            if user_type == 'client':
                return redirect('/client')
            elif user_type == 'manager':
                return redirect('/manager')
            elif user_type == 'admin':
                return redirect('/admin')
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect('/login')
    else:
        return render_template('index.html')



# Function to authenticate user against the database
def authenticate_user(email, password):
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM Administrator WHERE email = %s AND mot_de_passe = %s"
    cursor.execute(query, (email, password))
    admin = cursor.fetchone()
    if admin:
        return 'admin'

    query = "SELECT * FROM Manager WHERE email = %s AND mot_de_passe = %s"
    cursor.execute(query, (email, password))
    manager = cursor.fetchone()
    if manager:
        return 'manager'

    query = "SELECT * FROM Client WHERE email = %s AND mot_de_passe = %s"
    cursor.execute(query, (email, password))
    client = cursor.fetchone()
    if client:
        return 'client'

    return None

def get_stats():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) AS num_clients FROM Client")
    num_clients = cursor.fetchone()['num_clients']
    
    cursor.execute("SELECT COUNT(*) AS num_cars FROM Voiture")
    num_cars = cursor.fetchone()['num_cars']
    
    cursor.execute("SELECT COUNT(*) AS num_managers FROM Manager")
    num_managers = cursor.fetchone()['num_managers']
    
    cursor.execute("SELECT COUNT(*) AS num_reservations FROM Reservations")
    num_reservations = cursor.fetchone()['num_reservations']
    
    cursor.execute("SELECT COUNT(*) AS num_accepted FROM Reservations WHERE status = 'accepted'")
    num_accepted = cursor.fetchone()['num_accepted']
    
    cursor.execute("SELECT COUNT(*) AS num_refused FROM Reservations WHERE status = 'refused'")
    num_refused = cursor.fetchone()['num_refused']
    
    connection.close()
    
    return {
        'num_clients': num_clients,
        'num_cars': num_cars,
        'num_managers': num_managers,
        'num_reservations': num_reservations,
        'num_accepted': num_accepted,
        'num_refused': num_refused
    }

@app.route('/admin')
def admin():
    if 'email' in session:
        user_type = 'admin'
        stats = get_stats()
        return render_template('dashbord.html', user_type=user_type, stats=stats)
    else:
        return redirect('/login')

@app.route('/manager')
def manager():
    if 'email' in session:
        user_type = 'manager'
        stats = get_stats()
        return render_template('dashbord.html', user_type=user_type, stats=stats)
    else:
        return redirect('/login')


# Client route
# In the route for rendering client.html
@app.route('/client')
def client():
    if 'email' in session:
        client = session['client']  # Assuming 'client' is stored in the session
        
        # Fetch the refusal message for the client's reservation if it exists
        refusal_message = get_refusal_message(client['id_client'])
        accept_message = get_accept_message(client['id_client'])

        
        cars = get_cars()
        car = cars[0] if cars else None
        return render_template('client.html', cars=cars, car=car, client=client, refusal_message=refusal_message , accept_message=accept_message)
    else:
        return redirect('/login')

def get_refusal_message(client_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT refusal_message FROM Reservations WHERE id_client = %s AND status = 'refused'"
        cursor.execute(query, (client_id,))
        refusal_message = cursor.fetchone()
        connection.close()
        return refusal_message['refusal_message'] if refusal_message else None
    except Exception as e:
        logging.error("Error fetching refusal message: %s", str(e))
        return None

def get_accept_message(client_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT accept_message FROM Reservations WHERE id_client = %s AND status = 'accept'"
        cursor.execute(query, (client_id,))
        accept_message = cursor.fetchone()
        connection.close()
        return accept_message['accept_message'] if accept_message else None
    except Exception as e:
        logging.error("Error fetching refusal message: %s", str(e))
        return None








@app.route('/cars')
def cars():
    cars = get_cars()
    return render_template('voiture_list.html', cars=cars)

def get_cars():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Voiture")
        cars = cursor.fetchall()
        connection.close()
        return cars
    except Exception as e:
        logging.error("Error fetching cars: %s", str(e))
        return []
        
IMAGE_UPLOAD_FOLDER = os.path.join(app.static_folder, 'images')

@app.route('/add_car', methods=['POST'])
def add_car():
    if request.method == 'POST':
        # Get form data
        marque = request.form['marque']
        modele = request.form['modele']
        immatriculation = request.form['immatriculation']
        categorie = request.form['categorie']
        prix = request.form['prix']
        disponibilite = request.form['disponibilite']
        image = request.files['image_data']

        if not os.path.exists(IMAGE_UPLOAD_FOLDER):
            os.makedirs(IMAGE_UPLOAD_FOLDER)

        if image:
            filename = secure_filename(image.filename)
            # Save the file to the specific folder
            image.save(os.path.join(IMAGE_UPLOAD_FOLDER, filename))
        else:
            filename = None

        try:
            # Insert car data into the database
            connection = get_database_connection()
            cursor = connection.cursor()
            query = "INSERT INTO Voiture (marque, modele, immatriculation, categorie, prix, disponibilite, image_data) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (marque, modele, immatriculation, categorie, prix, disponibilite, filename))
            connection.commit()
            connection.close()
            return 'Car added successfully'
        except Exception as e:
            return 'Error adding car: ' + str(e)



@app.route('/delete_car', methods=['POST'])
def delete_car():
    if request.method == 'POST':
        try:
            # Get car ID from request data
            car_id = request.form['car_id']

            # Delete car from the database
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                query = "DELETE FROM Voiture WHERE id_voiture = %s"
                cursor.execute(query, (car_id,))
                connection.commit()
                connection.close()
                return 'Car deleted successfully'
            else:
                return 'Failed to establish database connection'
        except Exception as e:
            logging.error("Error deleting car: %s", str(e))
            return 'Error deleting car: ' + str(e)       

@app.route('/edit_car', methods=['POST'])
def edit_car():
    if request.method == 'POST':
        try:
            # Get form data
            car_id = request.form['car_id']
            marque = request.form['marque']
            modele = request.form['modele']
            immatriculation = request.form['immatriculation']
            categorie = request.form['categorie']
            prix = request.form['prix']
            disponibilite = request.form['disponibilite']

            # Update car information in the database
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()

                # Update car information excluding image
                query = "UPDATE Voiture SET marque = %s, modele = %s, immatriculation = %s, categorie = %s, prix = %s, disponibilite = %s WHERE id_voiture = %s"
                cursor.execute(query, (marque, modele, immatriculation, categorie, prix, disponibilite, car_id))

                connection.commit()
                connection.close()
                
                # Redirect to /admin route
                return redirect(url_for('admin'))
            else:
                return 'Failed to establish database connection'
        except Exception as e:
            logging.error("Error editing car: %s", str(e))
            return 'Error editing car: ' + str(e)






@app.route('/managers')
def managers():
    managers = get_managers()
    return render_template('manager_list.html', managers=managers)

@app.route('/clients')
def clients():
    """ Renders the list of clients """
    clients = get_clients()
    return render_template('client_list.html', clients=clients)


# Function to fetch clients from the database
def get_clients():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Client")
        clients = cursor.fetchall()
        connection.close()
        return clients
    except Exception as e:
        print("Error fetching clients:", e)
        return []

def get_cars():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Voiture")
        cars = cursor.fetchall()
        connection.close()
        return cars
    except Exception as e:
        print("Error fetching cars:", e)
        return []
# Route to add a manager
@app.route('/add_manager', methods=['POST'])
def add_manager():
    if request.method == 'POST':
        last_name = request.form['lastName']
        first_name = request.form['firstName']
        email = request.form['email']
        password = request.form['password']
        
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            query = "INSERT INTO Manager (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (last_name, first_name, email, password))
            connection.commit()
            connection.close()
            return 'Manager added successfully'
        except Exception as e:
            return 'Error adding manager: ' + str(e)

# Route to delete a manager
@app.route('/delete_manager', methods=['POST'])
def delete_manager():
    if request.method == 'POST':
        try:
            manager_id = request.form['manager_id']
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                query = "DELETE FROM Manager WHERE id_manager = %s"
                cursor.execute(query, (manager_id,))
                connection.commit()
                connection.close()
                return 'Manager deleted successfully'
            else:
                return 'Failed to establish database connection'
        except Exception as e:
            logging.error("Error deleting manager: %s", str(e))
            return 'Error deleting manager: ' + str(e)

@app.route('/edit_manager', methods=['POST'])
def edit_manager():
    if request.method == 'POST':
        manager_id = request.form['manager_id']
        last_name = request.form['lastName']
        first_name = request.form['firstName']
        email = request.form['email']
        password = request.form['password']
        
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            query = "UPDATE Manager SET nom = %s, prenom = %s, email = %s, mot_de_passe = %s WHERE id_manager = %s"
            cursor.execute(query, (last_name, first_name, email, password, manager_id))
            connection.commit()
            connection.close()
            return redirect('/admin')  # Redirect to /admin
        except Exception as e:
            # Handle the exception
            return 'Error updating manager: ' + str(e)




# Route to handle car reservation
def get_reservations():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Reservations")
        reservations = cursor.fetchall()
        connection.close()
        return reservations
    except Exception as e:
        logging.error("Error fetching reservations: %s", str(e))
        return []

# Route to display reservations

@app.route('/reservations')
def reservations():
    try:
        # Fetch reservations from the database
        reservations = get_reservations()
        return render_template('reservations.html', reservations=reservations)
    except Exception as e:
        logging.error("Error fetching reservations: %s", str(e))
        return 'Error fetching reservations: ' + str(e)


@app.route('/reserve_car', methods=['POST'])
def reserve_car():
    if request.method == 'POST':
        try:
            # Extract car ID and client ID from the request data
            car_id = request.form.get('carId')
            client_id = request.form.get('clientId')

            # Insert reservation data into the database with status "Pending"
            connection = get_database_connection()
            cursor = connection.cursor(dictionary=True)

            # Check if the car is already reserved
            query = "SELECT disponibilite FROM Voiture WHERE id_voiture = %s"
            cursor.execute(query, (car_id,))
            car = cursor.fetchone()
            if not car['disponibilite']:
                return 'Error reserving car: The car is already rented'

            # Insert reservation data with status "Pending"
            query = "INSERT INTO Reservations (id_voiture, id_client, status) VALUES (%s, %s, 'Pending')"
            cursor.execute(query, (car_id, client_id))

            connection.commit()
            connection.close()

            return 'Car reserved successfully'
        except Exception as e:
            logging.error("Error reserving car: %s", str(e))
            return 'Error reserving car: ' + str(e)

@app.route('/reservation/<int:reservation_id>', methods=['GET', 'POST'])
def view_reservation(reservation_id):
    if request.method == 'GET':
        try:
            connection = get_database_connection()
            cursor = connection.cursor(dictionary=True)

            # Fetch reservation details
            query = "SELECT * FROM Reservations WHERE id_reservation = %s"
            cursor.execute(query, (reservation_id,))
            reservation = cursor.fetchone()

            # Fetch car details
            query = "SELECT * FROM Voiture WHERE id_voiture = %s"
            cursor.execute(query, (reservation['id_voiture'],))
            car = cursor.fetchone()

            # Fetch client details
            query = "SELECT * FROM Client WHERE id_client = %s"
            cursor.execute(query, (reservation['id_client'],))
            client = cursor.fetchone()

            connection.close()

            return render_template('reservation.html', reservation=reservation, car=car, client=client)
        except Exception as e:
            logging.error("Error viewing reservation: %s", str(e))
            return 'Error viewing reservation: ' + str(e)
    elif request.method == 'POST':
        try:
            status = request.form['status']

            connection = get_database_connection()
            cursor = connection.cursor()

            # Update reservation status
            query = "UPDATE Reservations SET status = %s WHERE id_reservation = %s"
            cursor.execute(query, (status, reservation_id))

            if status == 'Accept':
                # Update car status to "Not Available"
                query = "UPDATE Voiture SET disponibilite = FALSE WHERE id_voiture = %s"
                cursor.execute(query, (reservation['id_voiture'],))

            connection.commit()
            connection.close()

            return redirect(url_for('view_reservation', reservation_id=reservation_id))
        except Exception as e:
            logging.error("Error updating reservation status: %s", str(e))
            return 'Error updating reservation status: ' + str(e)


def update_car_status(car_id, availability):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        query = "UPDATE Voiture SET disponibilite = %s WHERE id_voiture = %s"
        cursor.execute(query, (availability, car_id))
        connection.commit()
        connection.close()
    except Exception as e:
        logging.error("Error updating car status: %s", str(e))
        raise

# Update the update_reservation route
@app.route('/update_reservation/<int:reservation_id>', methods=['POST'])
def update_reservation(reservation_id):
    try:
        status = request.form['status'].lower()  # Convert to lowercase for consistency
        
        # Fetch reservation details
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Reservations WHERE id_reservations = %s"
        cursor.execute(query, (reservation_id,))
        reservation = cursor.fetchone()
        
        # Update reservation status and refusal message in the database
        query = "UPDATE Reservations SET status = %s, refusal_message = %s WHERE id_reservations = %s"
        cursor.execute(query, (status, request.form.get('refusal_message'), reservation_id))

        # Update car status based on reservation status
        if status == 'accepted':
            # Update car status to "Not Available"
            update_car_status(reservation['id_voiture'], False)
            
            # If any other reservations exist for the same car, set their status to "Refused"
            query = "UPDATE Reservations SET status = 'refused' WHERE id_voiture = %s AND id_reservations != %s"
            cursor.execute(query, (reservation['id_voiture'], reservation_id))
        elif status == 'refused':
            # Check if the car has any accepted reservations remaining
            query = "SELECT * FROM Reservations WHERE id_voiture = %s AND status = 'accepted'"
            cursor.execute(query, (reservation['id_voiture'],))
            remaining_accepted_reservations = cursor.fetchall()
            if not remaining_accepted_reservations:
                # If no other accepted reservations exist, update car status to "Available"
                update_car_status(reservation['id_voiture'], True)
        
        connection.commit()
        connection.close()

        return redirect('/admin')  # Redirect back to the reservations page
    except Exception as e:
        logging.error("Error updating reservation status: %s", str(e))
        return 'Error updating reservation status: ' + str(e)



@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    try:
        # Fetch reservation details
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Reservations WHERE id_reservations = %s"
        cursor.execute(query, (reservation_id,))
        reservation = cursor.fetchone()

        # Delete reservation from the database
        query = "DELETE FROM Reservations WHERE id_reservations = %s"
        cursor.execute(query, (reservation_id,))
        connection.commit()

        # Check if the deleted reservation was the only accepted reservation for the car
        if reservation['status'] == 'accepted':
            query = "SELECT * FROM Reservations WHERE id_voiture = %s AND status = 'accepted'"
            cursor.execute(query, (reservation['id_voiture'],))
            remaining_accepted_reservations = cursor.fetchall()
            if not remaining_accepted_reservations:
                # If no other accepted reservations exist, update car status to "Available"
                update_car_status(reservation['id_voiture'], True)

        connection.close()
        return redirect('/admin')
    except Exception as e:
        logging.error("Error deleting reservation: %s", str(e))
        return 'Error deleting reservation: ' + str(e)




@app.route('/')
def index():
    cars = get_cars()
    return render_template('index.html', cars=cars)


def get_managers():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Manager")
        cars = cursor.fetchall()
        connection.close()
        return cars
    except Exception as e:
        print("Error fetching managers:", e)
        return []

if __name__ == "__main__":
    app.run(debug=True)
