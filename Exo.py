from datetime import timedelta

from Essai import Essai


class Exo:
    # Attributs statiques de la classe Exo  stockant les:
    # --nombre total d'exos
    nbr_exos = 0
    # --nombre d'essais moyen des exos
    essais_moyen = 0

    # Instanciation d'un objet representatnt un exo
    def __init__(self, tp, exercice):
        # Incrémentation du nombre total d'exo
        Exo.nbr_exos += 1
        # les identifiants de l'exo (exercice et tp)
        self.exercice = exercice
        self.tp = tp
        # Le nombre d'essais de cet exo
        self.nbr_essais_exo = 0
        # liste des essais sur l'exercice par defaut vide
        self.essais = list()
        # Nombre d'echecs sur l'exo
        self.nbr_echecs = 0
        # Nombre de réussites sur l'exo
        self.nbr_reussites = 0
        # Dictionnaire des étudiants qui ont tentés l'exo et des (exo, nbre_tentatives_sur_lexo,
        # nbre_echecs_sur_lexo, nbre_reussites _sur_lexo, date_premier_essai_periode_pour_reussir)
        self.etudiants = {}
        # --Temps moyen mis par un étudiant pour réussir cet exercice
        self.temps_moyen_reussite = None
        # Nombre de fois q'un étudiant a resolu l'exo en une seul tentative
        self.resolu_dun_coup = 0

    def tenter(self, essai):
        # Incrémentation du nombre d'essais selon l'exercice et update de la moyenne des essais par exercice
        self.nbr_essais_exo += 1
        Exo.essais_moyen = Essai.essais / Exo.nbr_exos
        # Ajout de l'essai dans la liste d'essai
        self.essais.append(essai)
        essai_reussi = 0
        essai_echoue = 0
        # Si l'essai a reussi
        if essai.essai_reussi:
            self.nbr_reussites += 1
            essai_reussi = 1
        else:
            self.nbr_echecs += 1
            essai_echoue = 1
        # On verifie si l'etudiant correspondant à l'essai ne fait pas déja parti de notre dictionnaire d'etudiants sur l'exo
        e = None
        for id_etudiant in self.etudiants.keys():
            # Si l'etudiant fait déja parti de notre dictionnaire d'étudiants sur l'exo
            if id_etudiant == essai.etudiant.id_etudiant:
                e = id_etudiant
                # Si l'exo est réussi, on calcul
                # la periode entre le premier essai d’un étudiant et sa réussite
                periode = None
                (tp, exercice, tentatives, echecs, reussites, date_premier_essai, periode_pour_reussir) = \
                self.etudiants[id_etudiant]
                if essai_reussi == 1 and periode_pour_reussir is None:
                    periode = essai.date - date_premier_essai
                    # Incrémentation du Temps moyen mis par un étudiant pour réussir cet exercice
                    if self.temps_moyen_reussite is None:
                        self.temps_moyen_reussite = periode / len(self.etudiants.keys())
                    else:
                        self.temps_moyen_reussite += periode / len(self.etudiants.keys())
                self.etudiants[id_etudiant] = (tp, exercice,
                                               tentatives + 1, echecs + essai_echoue, reussites + essai_reussi,
                                               date_premier_essai, periode)
                break
        # Si l'etudiant ne fait pas parti de notre dictionnaire d'étudiants sur l'exo
        # premier essai d’un étudiant ____________________________________
        if e is None:
            periode = None
            # si l'étudiant reussi l'exo en seul essai
            if essai_reussi == 1:
                self.resolu_dun_coup += 1
                periode = timedelta(days=0, hours=0, minutes=0, seconds=0)
                if self.temps_moyen_reussite is None:
                    self.temps_moyen_reussite = timedelta(days=0, hours=0, minutes=0, seconds=0)
                else:
                    self.temps_moyen_reussite += timedelta(days=0, hours=0, minutes=0, seconds=0)
            self.etudiants[essai.etudiant.id_etudiant] = (
                self.tp, self.exercice, 1, essai_echoue, essai_reussi, essai.date, periode)