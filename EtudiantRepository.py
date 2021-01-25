class EtudiantRepository:

    def __init__(self):
        # La liste des étudiants distincts, par defaut vide
        # sera mise à jour après chaque essai d'un étudiant
        self.etudiants = list()
