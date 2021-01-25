from Essai import Essai

class Etudiant:
    #Attributs statiques de la classe Etudiant stockant les:
    #--nombre total d'étudiants ayant effectué au moins un essai
    nbr_etudiants = 0
    #--nombre d'essais moyen des étudiants
    essais_moyen = 0
    #exercices essayés mais réussis par aucun étudiant
    exercices = list()

    #Instanciation d'un objet representatnt un étudiant
    def __init__(self, groupe, id_etudiant):
        #Incrémentation du nombre total d'étudiants
        Etudiant.nbr_etudiants += 1
        #Incrémentation du nombre total d'étudiants dans leur groupe
        groupe.adhesion(self)
        #Identifiant de l'étudiant et de son groupe
        self.id_etudiant = id_etudiant
        self.groupe = groupe
        #Le nombre d'essais effectué par l'étudiant
        self.nbr_essais = 0
        #Le nombre de succes effectué par l'étudiant
        self.nbr_succes = 0
        #liste des essais de l'étudiant par defaut vide
        self.essais = list()
        # Dictionnaire des exercices tentés par cet étudiant et du nombre de tentatives pour chaque exercice
        self.exercices = {}
        # Dictionnaire des exercices reussis par cet étudiant
        self.reussites = {}

    def tenter(self, essai):
        # Incrémentation du nombre d'essais selon l'étudiant et update de la moyenne des essais
        self.nbr_essais += 1
        Etudiant.essais_moyen = Essai.essais / Etudiant.nbr_etudiants
        #Ajout de l'essai dans la liste d'essai
        self.essais.append(essai)
        # On verifie si l'exo correspondant à l'essai ne fait pas déja parti de notre dictionnaire d'exercices tentés
        e = None
        for exo in self.exercices.keys():
            # Si l'exo tenté fait déja parti de notre liste
            if exo.exercice==essai.exo.exercice and exo.tp==essai.exo.tp :
                e = exo
                self.exercices[exo] += 1
                if essai.essai_reussi:
                    #prise en compte de la multi-validation du même exercice par un étudiant
                    if self.reussites[exo]==False:
                        self.nbr_succes += 1
                    self.reussites[exo] = True
                else:
                    self.reussites[essai.exo] = False
                break
        # Si l'exo tenté ne fait pas parti de notre dictionnaire
        if e is None:
            self.exercices[essai.exo] = 1
            if essai.essai_reussi:
                self.reussites[essai.exo] = True
                self.nbr_succes += 1
            else:
                self.reussites[essai.exo] = False
