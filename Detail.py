class Detail:

    def __init__(self, essai, date, nom_test, message):
        self.essai = essai
        self.date = date
        #nom de la fonction exécutée qui correspond au test unitaire
        self.nom_test = nom_test
        #le message d’erreur lié au test, si échec
        self.message = message
        essai.details.append(self)

