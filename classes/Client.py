class Client:
    def __init__(self, id, nom, prenom, email, ):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.reservations = []

    def get_reservations(self):
        return self.reservations

    def reserver_voiture(self, voiture):
        if voiture.reserve():
            self.reservations.append(voiture)
            return True
        else:
            return False

    def annuler_reservation(self, voiture):
        if voiture in self.reservations:
            self.reservations.remove(voiture)
            voiture.annuler_reservation()
