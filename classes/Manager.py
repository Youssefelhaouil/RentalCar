class Manager:
    def __init__(self, id_manager, nom, prenom, email, mot_de_passe):
        self.id_manager = id_manager
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe
        # List of cars
        self.voitures = []
        # List of reservations
        self.reservations = []

    def get_cars(self):
        return self.voitures

    def add_car(self, voiture):
        self.voitures.append(voiture)
        print("Voiture ajoutée avec succès.")

    def modify_car(self, id_voiture, new_car_info):
        for voiture in self.voitures:
            if voiture.id_voiture == id_voiture:
                voiture.marque = new_car_info['marque']
                voiture.modele = new_car_info['modele']
                voiture.immatriculation = new_car_info['immatriculation']
                voiture.categorie = new_car_info['categorie']
                voiture.prix = new_car_info['prix']
                print("Voiture modifiée avec succès.")
                return
        print("Voiture non trouvée.")

    def delete_car(self, id_voiture):
        for i, voiture in enumerate(self.voitures):
            if voiture.id_voiture == id_voiture:
                del self.voitures[i]
                print("Voiture supprimée avec succès.")
                return
        print("Voiture non trouvée.")

    def get_reservations(self):
        return self.reservations

    def accept_reservation(self, reservation):
        if reservation in self.reservations:
            self.reservations.remove(reservation)
            print("La réservation a été acceptée.")
        else:
            print("La réservation n'existe pas.")

    def refuse_reservation(self, reservation):
        if reservation in self.reservations:
            self.reservations.remove(reservation)
            print("La réservation a été refusée.")
        else:
            print("La réservation n'existe pas.")
