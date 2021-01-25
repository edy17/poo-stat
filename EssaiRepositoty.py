import csv
from collections import namedtuple
from datetime import datetime

from Essai import Essai
from Groupe import Groupe
from Etudiant import Etudiant

EssaiData = namedtuple("EssaiData",
                       "date id exercice id_etudiant groupe nbre_erreurs nbre_echecs nbre_tests duree_essai code_sorti")


class EssaiRepository:

    def __init__(self, exoRepository, groupeRepository, etudiantRepository):

        # La liste des essais, par defaut vide
        self.essais = list()
        # Le repository contenant la liste de tous les groupes distincts
        self.groupeRepository = groupeRepository
        # Le repository contenant la liste de tous les etudiants distincts
        self.etudiantRepository = etudiantRepository
        # Le repository contenant la liste de tous les exos distincts
        self.exoRepository = exoRepository

        # Lecture du fichier de données essais.csv en modèle de données
        # et chargement des modèles de domaines
        csv.register_dialect('myDialect', delimiter=';')
        with open('essais.csv', 'r') as file:
            # Lecture du fichier essais.csv
            reader = csv.reader(file, dialect='myDialect')
            # Lecture des colones de chaque ligne dans une liste de tuples nommés et chargement des listes
            datas = [EssaiData(*r) for r in reader]
            # Pour chaque ligne lue
            for data in datas:
                # Identification de l'exo tenté à travers une boucle
                # Pour chaque exo tenté
                for exo in self.exoRepository.exos:
                    # Si l'exo correspond à l'id lu
                    if exo.exercice == data.exercice:
                        # On initialise un groupe vide et un étudiant vide
                        g = None
                        e = None
                        # Identification du groupe de l'étudiant qui a effectué l'essai, à travers une bouclee
                        # Ou creation d'un nouveau groupe si premier occurence du groupe dans la lecture
                        for groupe in self.groupeRepository.groupes:
                            # On recupère le groupe correspondant à l'essai si le groupe existe
                            if data.groupe == groupe.id:
                                g = groupe
                                break
                        # On crée le nouveau groupe correspondant à l'essai si il n'existe pas encore,
                        # puis on l'ajoute dans sa liste
                        if g is None:
                            g = Groupe(data.groupe)
                            self.groupeRepository.groupes.append(g)
                        # Identification de l'étudiant qui a effectué l'essai, à travers une bouclee
                        # Ou creation d'un nouvel étudiant si premier occurence de l'étudiant dans la lecture
                        for etudiant in self.etudiantRepository.etudiants:
                            # On recupère l'étudiant correspondant à l'essai s'il existe
                            if data.id_etudiant == etudiant.id_etudiant:
                                e = etudiant
                                break
                        # On crée le nouvel étudiant correspondant à l'essai s'il n'existe pas
                        # puis on l'ajoute dans sa liste
                        if e is None:
                            e = Etudiant(g, data.id_etudiant)
                            self.etudiantRepository.etudiants.append(e)
                        # On crèe l'objet date
                        datetime_object = datetime.strptime(data.date, '%d/%m/%Y %H:%M:%S')
                        # On crée l'essai
                        essai = Essai(data.id, exo, datetime_object, e, g, data.nbre_erreurs, data.nbre_echecs,
                                      data.nbre_tests,
                                      data.duree_essai,
                                      data.code_sorti)
                        # on ajoute dans la liste d'essais
                        self.essais.append(essai)
                        break
