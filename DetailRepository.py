import csv
from collections import namedtuple

from Detail import Detail

DetailData = namedtuple("DetailData", "date essai_id exercice etudiant groupe nom_test durée message")


class DetailRepository:

    def __init__(self, essaiRepository):
        self.details = list()
        self.essaiRepository = essaiRepository
        csv.register_dialect('myDialect', delimiter=';')
        with open('details.csv', 'r') as file:
            reader = csv.reader(file, dialect='myDialect')
            datas = [DetailData(*r) for r in reader]
            for data in datas:
                for essai in self.essaiRepository.essais:
                    if essai.id == data.essai_id:
                        detail = Detail(essai, data.date, data.nom_test, data.message)
                        self.details.append(detail)
                        break
