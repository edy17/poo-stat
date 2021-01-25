import csv

from Exo import Exo


class ExoRepository:

    def __init__(self):
        csv.register_dialect('myDialect', delimiter=';')
        with open('exos.csv', 'r') as file:
            reader = csv.reader(file, dialect='myDialect')
            # La liste des exos distincts, par defaut vide
            # sera mise à jour après chaque essai d'un étudiant
            # pour reduire le temps d'exécution
            self.exos = [Exo(*r) for r in reader]
