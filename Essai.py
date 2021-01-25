class Essai:
    #Attribut statique de la classe Essai  stocckant le:
    #nombre d'essais total
    essais = 0

    #Instanciation d'un objet representatnt un essai
    #Un objet Essai met en relation un objet Exo avec deux objets Groupe et Etudiant
    def __init__(self, id, exo, date, etudiant, groupe, nbre_erreurs, nbre_tests_echoues, nbre_tests, duree_essai,
                 code_sorti):
        #Incrémentation du nombre total d'essais
        Essai.essais += 1
        self.id = id
        self.etudiant = etudiant #Objet concerné par l'essai
        self.groupe = groupe #Objet concerné par l'essai
        self.exo = exo #Objet concerné par l'essai
        self.date = date
        self.nbre_erreurs = nbre_erreurs
        self.nbre_tests_echoues = nbre_tests_echoues
        self.nbre_tests = nbre_tests
        self.duree_essai = duree_essai
        self.code_sorti = code_sorti
        # liste des details sur les test unitaires de l'essai
        self.details = list()
        #Drapeau pour verifier si l'essai est réussi ou échoué
        self.essai_reussi = False
        self.essai_echoue = True
        # Si tous les tests unitaires ont réussis et il n'y a pas eut de plantage
        if int(nbre_tests_echoues)==0 and int(nbre_erreurs)==0:
            self.essai_reussi = True
            self.essai_echoue = False
        #On applique l'essai en cascade sur le groupe, l'étudiant et l'exo lié à l'essai
        self.exo.tenter(self)
        self.groupe.tenter(self)
        self.etudiant.tenter(self)


