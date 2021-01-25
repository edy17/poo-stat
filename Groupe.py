from Essai import Essai


class Groupe:
    # Attributs statiques de la classe Groupe stockant les:
    # --nombre total de groupes  ayant effectué au moins un essai
    nbr_groupes = 0
    # --nombre d'essais moyen des groupes
    essais_moyen = 0

    # Instanciation d'un objet representatnt un groupe
    def __init__(self, id):
        # Incrémentation du nombre total de groupes
        Groupe.nbr_groupes += 1
        # l'identifiant du groupe
        self.id = id
        # Le nombre d'étudiants du groupe par defaut nulle
        self.nbr_etudiants = 0
        # liste des etudiants du groupe par defaut vide
        self.etudiants = list()
        # Le nombre d'essais effectué par le groupe
        self.nbr_essais = 0
        # liste des essais du groupe par defaut vide
        self.essais = list()
        # Dictionnaire des exercices tentés par ce groupe et du nombre de tentatives pour chaque exercice
        self.exercices = {}

    def adhesion(self, etudiant):
        # Incrémentation du nombre total d'étudiants dans le groupe
        self.nbr_etudiants += 1
        self.etudiants.append(etudiant)

    def tenter(self, essai):
        # Incrémentation du nombre d'essais selon le gropue et update de la moyenne des essais par groupe
        self.nbr_essais += 1
        Groupe.essais_moyen = Essai.essais / Groupe.nbr_groupes
        # Identification de l'exo tenté à travers une boucle
        # Ajout de l'essai dans la liste d'essai
        self.essais.append(essai)
        # On verifie si l'exo correspondant à l'essai ne fait pas déja parti de notre dictionnaire d'exercices tentés
        e = None
        for exo in self.exercices.keys():
            # Si l'exo tenté fait déja parti de notre liste
            if exo.exercice == essai.exo.exercice and exo.tp == essai.exo.tp:
                e = exo
                self.exercices[exo] += 1
                break
        # Si l'exo tenté ne fait pas parti de notre dictionnaire
        if e is None:
            self.exercices[essai.exo] = 1

