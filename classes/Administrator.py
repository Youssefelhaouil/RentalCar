class Administrator:
    def __init__(self, admin_id, nom, prenom, email, mot_de_passe):
        self.admin_id = admin_id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.managers_managed = []

    def get_managers(self):
        return self.managers_managed

    def add_manager(self, manager_details):
        self.managers_managed.append(manager_details)

    def modify_manager(self, manager_id, new_details):
        for manager in self.managers_managed:
            if manager.manager_id == manager_id:
                manager._dict_.update(new_details)

    def delete_manager(self, manager_id):
        self.managers_managed = [manager for manager in self.managers_managed if manager.manager_id != manager_id]
