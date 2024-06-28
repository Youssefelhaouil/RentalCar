from main import *
class Voiture:
    def __init__(self, id_voiture, marque, modele, immatriculation, categorie, prix, disponibilite=True):
        self.id_voiture = id_voiture
        self.marque = marque
        self.modele = modele
        self.immatriculation = immatriculation
        self.categorie = categorie
        self.prix = prix
        self.disponibilite = disponibilite



    def get_cars(self):
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

    @app.route('/')
    def index():
        cars = get_cars()
        return render_template('index.html', cars=cars)

    def reserve(self):

        if self.disponibilite:
            self.disponibilite = True
            return False

    def annuler_reservation(self):
        if self.disponibilite == False:
            return self.disponibilite == True


