import json
from Manager import Manager
from Administrator import Administrator
from Client import Client
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'client': [], 'manager': [], 'administrator': []}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def generate_id(role, users):
    if role == "client":
        prefix = "CL"
    elif role == "manager":
        prefix = "MN"
    elif role == "administrator":
        prefix = "AD"
    else:
        raise ValueError("Invalid role")

    # Find the highest ID for the given role
    max_id = 0
    for user in users[role]:
        user_id = int(user.get('id')[2:])  # Extract numeric part of ID
        max_id = max(max_id, user_id)

    return f"{prefix}{max_id + 1:04d}"  # Format ID with leading zeros

def login():
    print("Welcome to the car rental system!")
    choice = input("Do you want to login or sign up? (login/signup): ").lower()

    if choice == "login":
        email = input("Enter your email: ")

        # Load users from file
        users = load_users()

        # Check if email exists
        user_found = False
        for role, user_list in users.items():
            for user in user_list:
                if user['user_info']['email'] == email:
                    print(f"Logged in as {user['role'].capitalize()}.")
                    if user['role'] == 'manager':
                        manager_instance = Manager(user['id'], user['user_info']['first_name'], user['user_info']['last_name'], user['user_info']['email'], user['user_info']['password'])
                        options = show_options(user['role'])
                        perform_action(options, manager_instance)
                    elif user['role'] == 'administrator':
                        administrator_instance = Administrator(user['id'], user['user_info']['first_name'], user['user_info']['last_name'], user['user_info']['email'], user['user_info']['password'])
                        options = show_options(user['role'])
                        perform_action(options, administrator_instance)
                    else:  # For client
                        client_instance = Client(user['id'], user['user_info']['first_name'], user['user_info']['last_name'], user['user_info']['email'])
                        options = show_options(user['role'])
                        perform_action(options, client_instance)
                    user_found = True
                    break

        if not user_found:
            print("Invalid email. Please try again.")
            login()
    elif choice == "signup":
        signup()
    else:
        print("Invalid choice. Please try again.")
        login()

def perform_action(options, user_instance):
    print("Select an option:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option.replace('_', ' ').title()}")
    choice = input("Enter your choice: ")
    try:
        choice = int(choice)
        getattr(user_instance, options[choice - 1])()
    except (ValueError, IndexError):
        print("Invalid choice. Please try again.")
        perform_action(options, user_instance)

def show_options(role):
    options = []
    if role == "client":
        options = [
            "get_reservations",
            "reserve_car",
            "cancel_reservation"
        ]
    elif role == "manager":
        options = [
            "get_cars",
            "add_car",
            "modify_car",
            "delete_car",
            "get_reservations",
            "accept_reservation",
            "refuse_reservation"
        ]
    elif role == "administrator":
        options = [
            "get_managers",
            "add_manager",
            "modify_manager",
            "delete_manager"
        ]
    return options

def signup():
    print("Sign Up")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    role = input("Choose your role (client/manager): ").lower()

    # Check if email already exists
    users = load_users()
    for user in users[role]:
        if user['user_info']['email'] == email:
            print("Email already exists. Please choose a different email.")
            return

    # For manager, set password
    if role == 'manager':
        password = input("Set your password: ")
    else:
        password = None

    # Generate ID based on role
    user_id = generate_id(role, users)

    # Create a new user dictionary
    new_user = {
        'role': role,
        'id': user_id,
        'user_info': {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password  # Only set password for managers
        }
    }

    # Add new user to the list of users in the respective sector
    users[role].append(new_user)

    # Save updated user list to file
    save_users(users)

    print(f"Signed up as {role.capitalize()}. You can now login.")


if __name__ == "__main__":
    login()
