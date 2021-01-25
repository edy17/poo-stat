import calendar
import json
import operator
from collections import OrderedDict
from datetime import timedelta, datetime

from EtudiantRepository import EtudiantRepository
from ExoRepository import ExoRepository
from EssaiRepositoty import EssaiRepository
from DetailRepository import DetailRepository
from GroupeRepository import GroupeRepository
from Etudiant import Etudiant
from Groupe import Groupe


# Chargement des données à parir des fichiers csv.

# Les données sont encapsulées dans des classes métiers(package domain)
# sémantiquement liés par des relations du type OneToMany et ManyToOne.

# Les objets metiers stockent les données brutes et des statistiques sur ses données.

# Chaque classe métier a un repository(package repository)
# qui ouvre les fichiers csv, et charge les données ves des listes specifiques,
# en respectant les liens sémantiques entre les objets métiers

# dataLoading recupère les listes spécifiques à chaque classe métier
# et les renvois dans un n-tuple
def dataLoading():
    exoRepository = ExoRepository()  # Contient la liste des exo distincts
    groupeRepository = GroupeRepository()  # Contient la liste des groupes distincts, vide par defaut
    etudiantRepository = EtudiantRepository()  # Contient la liste des étudiants distincts, vide par defaut
    # essaiRepository contient la liste des essais et
    # met à jours la listes groupes, des étudiants et des exo distincts
    essaiRepository = EssaiRepository(exoRepository, groupeRepository, etudiantRepository)
    detailRepository = DetailRepository(essaiRepository)  # Contient la liste des détails
    return (exoRepository.exos, groupeRepository.groupes, etudiantRepository.etudiants, essaiRepository.essais,
            detailRepository.details)


# _____________________________________________________________Les groupes
# 1)	Nombre d’étudiants par groupe de TP
def etudiantsParGroupe(groupesDistincts):
    temp = {}
    for groupe in groupesDistincts:
        temp[groupe.id] = groupe.nbr_etudiants
    return json.dumps({'Nombre d_etudiants Par Groupe': temp}, indent=1)


# 2)	Nombre de tentatives par groupe
def tentativesParGroupe(groupesDistincts):
    temp = {}
    for groupe in groupesDistincts:
        temp[groupe.id] = groupe.nbr_essais
    return json.dumps({'Nombre de tentatives par groupe': temp}, indent=1)


# 3)	Dictionnaire des groupes et de leurs nombres total de tentatives triés
#       par ordre décroissant du nombre de tentatives
def tentativesParGroupeTries(groupesDistincts):
    groupesTries = sorted(groupesDistincts, key=lambda groupe: groupe.nbr_essais, reverse=True)
    temp = {}
    for groupe in groupesTries:
        temp[groupe.id] = groupe.nbr_essais
    return json.dumps({'Dictionnaire des groupes tries selon leurs nombres total de tentatives': temp}, indent=1)


# _____________________________________________________________Les étudiants
# 1)	Déterminez le nombre moyen de tentatives par étudiant
def tentativesMoyensParEtudiant():
    return json.dumps({'Nombre moyen de tentatives par etudiant': Etudiant.essais_moyen}, indent=1)


# 2)	Effectuez le même calcul, mais par groupe et par étudiant
def tentativesMoyensParGroupe():
    return json.dumps({'Nombre moyen de tentatives par groupe': Groupe.essais_moyen}, indent=1)


# 3)	Retenez les 4 groupes les plus actifs pour la suite
def groupesPlusActifs(groupesDistincts):
    groupesTries = sorted(groupesDistincts, key=lambda groupe: groupe.nbr_essais, reverse=True)
    groupesActifs = list()
    groupesActifs.append(groupesTries[0])
    groupesActifs.append(groupesTries[1])
    groupesActifs.append(groupesTries[2])
    groupesActifs.append(groupesTries[3])
    temp = {}
    for groupe in groupesActifs:
        temp[groupe.id] = groupe.nbr_essais
    return json.dumps({'Les 4 groupes les plus actifs': temp}, indent=1)


# ________________________________________________________________Les exercices
# ________________________________________________________________Les échecs
# 1)	Déterminez la liste des exercices effectués, par groupe
def exercicesParGroupe(groupesDistincts):
    temp = {}
    for groupe in groupesDistincts:
        temp2 = list()
        for exo, tentatives in groupe.exercices.items():
            temp2.append(exo.tp + ", " + exo.exercice)
        temp[groupe.id] = temp2
    return json.dumps({'Liste d_exercices effectues par groupe': temp}, indent=1)


# 2)	Quels exercices ont été essayés mais réussis par aucun étudiant ?
def exercicesJamaisReussis(exosDistincts):
    temp = {}
    # Pour chaque exercice jamais reussis
    for exo in exosDistincts:
        if exo.nbr_essais_exo == exo.nbr_echecs:
            temp[exo.tp.split(" - ")[1] + "-" + exo.exercice.split(" - ")[0]] = exo.nbr_essais_exo
    return json.dumps({'Exercices jamais reussis': temp}, indent=1)


# 3)	(> Inutile) Combien de tentatives au total sur ces exercices ?
def tentativesEchecs(exosDistincts):
    # Tentatives au total sur les exercices qui ont été essayés mais réussis par aucun étudiant
    echecs = 0
    # Pour chaque exercice jamais reussis
    for exo in exosDistincts:
        if exo.nbr_essais_exo == exo.nbr_echecs:
            echecs += exo.nbr_essais_exo
    return json.dumps({'Nombre de tentatives total sur les exercices jamais reussis': echecs}, indent=1)


# 4)	(> Inutile) Combien de tentatives par étudiant sur ces exercices ?
def tentativesParEtudiantSurExoJamaisReussis(exosDistincts):
    temp = {}
    # Pour chaque exercice jamais reussis
    for exo in exosDistincts:
        if exo.nbr_essais_exo == exo.nbr_echecs:
            # Tentatives par étudiant sur chaque exercice échoué
            temp2 = {}
            for etudiant, (
                    tentatives, echecs, reussites, date_premier_essai,
                    periode_pour_reussir) in exo.etudiants.items():
                temp2[etudiant.id_etudiant] = tentatives
            temp[exo.tp.split(" - ")[1] + "-" + exo.exercice.split(" - ")[0]] = temp2
    return json.dumps({"Tentatives par etudiant sur chaque exercice jamais reussis": temp}, indent=1)


# ________________________________________________________________Les réussites
# 1)	Déterminez, pour chacun des exercices réussis au moins une fois, le temps moyen entre le premier essai d’un étudiant et sa réussite
def tempsMoyenReussiteParExo(exosDistincts):
    temp = {}
    # Pour chaque exercice  reussis
    for exo in exosDistincts:
        if exo.nbr_reussites > 0:
            minutes, seconds = divmod(exo.temps_moyen_reussite.seconds + exo.temps_moyen_reussite.days * 86400,
                                      60)
            hours, minutes = divmod(minutes, 60)
            days = hours // 24
            hours = hours % 24
            temp[
                exo.tp.split(" - ")[1] + "-" + exo.exercice.split(" - ")[
                    0]] = "{}jours,{}heures,{}minutes,{}secondes".format(
                days, hours, minutes, seconds)
    return json.dumps({'Temps moyen de reussite par exercice': temp}, indent=1)


# 2)	Quels exercices ont été le mieux réussis ?
def mieuxReussis(exosDistincts):
    # Liste des exercices qui ont été essayés et réussis au moins une fois par un étudiant
    reussites = list()
    temp = {}
    # Pour chaque exercice  reussis
    for exo in exosDistincts:
        if exo.nbr_reussites > 0:
            reussites.append(exo)
    # Liste des exercices qui ont été essayés et réussis au moins une fois par un étudiant
    # par ordre croissant du temps moyen de reussite
    meilleurs = sorted(reussites, key=lambda exo: exo.temps_moyen_reussite)
    for exo in meilleurs:
        minutes, seconds = divmod(exo.temps_moyen_reussite.seconds + exo.temps_moyen_reussite.days * 86400,
                                  60)
        hours, minutes = divmod(minutes, 60)
        days = hours // 24
        hours = hours % 24
        temp[exo.tp.split(" - ")[1] + "-" + exo.exercice.split(" - ")[
            0]] = "{}jours,{}heures,{}minutes,{}secondes".format(
            days, hours, minutes, seconds)
    return json.dumps({'Exercices reussis par ordre croissant du temps moyen de reussite': temp}, indent=1)


# 3)	Combien d’étudiants ont réussis des exercices en un seul essai ?
def nombreMeilleursEtudiants(exosDistincts):
    # Liste des étudiants qui ont réussi des exercices en un seul essai
    meilleurs = list()
    # Pour chaque exercice  reussis
    for exo in exosDistincts:
        if exo.nbr_reussites > 0:
            for id_etudiant in exo.etudiants.keys():
                (tp, exercice, tentatives, echecs, reussites, date_premier_essai, periode_pour_reussir) = \
                    exo.etudiants[id_etudiant]
                periodeNulle = timedelta(days=0, hours=0, minutes=0, seconds=0)
                if periode_pour_reussir is not None:
                    if periodeNulle.total_seconds() == periode_pour_reussir.total_seconds():
                        if id_etudiant not in meilleurs:
                            meilleurs.append(id_etudiant)
    return json.dumps({'Nombre etudiants ayant reussi des exercices en un seul essai': len(meilleurs)}, indent=1)


# _______________________________________________________________Les pics d’utilisation
# ________________________________________________________________En temps normal
# 1)	Dans une semaine normale, quels sont les jours où l’outil a été le plus utilisé ?
def picDUtilisationParJourSemaine(essais):
    # Dictionnaire des jours de la semaine où l'outils a été utilisé
    # et du nombre de tentatatives pour chaque jour  triées par ordre décroissant du nombre de tentatives
    weeks = {}
    for essai in essais:
        # jour de la semaine
        weekDay = calendar.day_name[essai.date.weekday()]
        if weekDay not in weeks.keys():
            weeks[weekDay] = 1
        else:
            weeks[weekDay] += 1
    # Trie par ordre décroissant du nombre de tentatipas par jour de la semaine
    weeks_descending = OrderedDict(sorted(weeks.items(),
                                          key=lambda x: x[1], reverse=True))
    return json.dumps({'Jours ou l_outil a ete le plus utilise': weeks_descending}, indent=1)


# 2)	Idem, mais pour les horaires ?
def picDUtilisationParHorraire(essais):
    # Dictionnaire des des heures de la journée où l'outils a été utilisé
    # et du nombre de tentatatives par heure  triées par ordre décroissant du nombre de tentatives
    hours = {}
    for essai in essais:
        # heure de la journée entre 0h et 24h
        hourDay = str(essai.date.hour) + "h"
        if hourDay not in hours.keys():
            hours[hourDay] = 1
        else:
            hours[hourDay] += 1
    # Trie par ordre décroissant du nombre de tentatipas par jour de la semaine
    hours_descending = OrderedDict(sorted(hours.items(),
                                          key=lambda x: x[1], reverse=True))
    return json.dumps({'Horaires ou l_outil a ete le plus utilise': hours_descending}, indent=1)


# 3)	Pour chaque jour de la semaine, quel est l’horaire qui contient le plus de tentatives ?
def picHoraireParJourSemaine(essais):
    # Dictionnaire des jours de la semaine où l'outils a été utilisé
    weeks = {}
    houurs = {}
    for essai in essais:
        # jour de la semaine
        weekDay = calendar.day_name[essai.date.weekday()]
        # heure de la journée entre 0h et 24h
        hourDay = str(essai.date.hour) + "h"
        if weekDay not in weeks.keys():
            # Dictionnaire des des heures de la journée où l'outils a été utilisé
            weeks[weekDay] = {}
            weeks[weekDay][hourDay] = 1
        else:
            if hourDay not in weeks[weekDay].keys():
                weeks[weekDay][hourDay] = 1
            else:
                weeks[weekDay][hourDay] += 1
    temp = {}
    for week in weeks.keys():
        temp[week] = max(weeks[week].items(), key=operator.itemgetter(1))[0]
    return json.dumps({'horaire ou l_outil a ete le plus utilise pour chaque jour de la semaine': temp}, indent=1)


# _________________________________________________________________En examens
# Les examens se sont déroulés du 22 au 26 octobre, et du 10 au 14 décembre
# 1)	Remarquez-vous un pic d’utilisation de l’outil pendant ces périodes ?
# ______________Reponse____________On remarque
# Pic d'utilisation en période d'examen
def picDUtilisationEnExamen(essais):
    # dates d'examens
    a1 = datetime.strptime('22/10/2018', '%d/%m/%Y')
    a2 = datetime.strptime('26/10/2018', '%d/%m/%Y')
    b1 = datetime.strptime('10/12/2018', '%d/%m/%Y')
    b2 = datetime.strptime('14/12/2018', '%d/%m/%Y')
    # Dictionnaire des jours où l'outils a été utilisé en periode d'examen
    # et du nombre de tentatatives par jour  triées par ordre décroissant du nombre de tentatives
    jours = {}
    for essai in essais:
        # Jour de l'essai
        day = essai.date.day
        month = essai.date.month
        year = essai.date.year
        jour = str(day) + "/" + str(month) + "/" + str(year)
        if a1 < essai.date < a2 or b1 < essai.date < b2:
            if jour not in jours.keys():
                jours[jour] = 1
            else:
                jours[jour] += 1
    # Trie par ordre décroissant du nombre de tentatives par jour de la periode d'examen
    jours_descending = OrderedDict(sorted(jours.items(),
                                          key=lambda x: x[1], reverse=True))
    return json.dumps(
        {'Pic d_utilisation en periode d_examen par ordre decroissant du nbre de tentatives': jours_descending},
        indent=1)


# 2)	Si oui, sur quels jours spécifiques ? Et quels horaires ?
def picHoraireEnExamen(essais):
    # dates d'examens
    a1 = datetime.strptime('22/10/2018', '%d/%m/%Y')
    a2 = datetime.strptime('26/10/2018', '%d/%m/%Y')
    b1 = datetime.strptime('10/12/2018', '%d/%m/%Y')
    b2 = datetime.strptime('14/12/2018', '%d/%m/%Y')
    # Dictionnaire des jours en periode d'examen où l'outils a été utilisé
    jours = {}
    for essai in essais:
        # Jour de l'essai
        day = essai.date.day
        month = essai.date.month
        year = essai.date.year
        jour = str(day) + "/" + str(month) + "/" + str(year)

        # heure de la journée entre 0h et 24h
        hourDay = str(essai.date.hour) + "h"
        if a1 < essai.date < a2 or b1 < essai.date < b2:
            if jour not in jours.keys():
                jours[jour] = {}
                jours[jour]['Total'] = 1
                jours[jour][hourDay] = 1
            else:
                if hourDay not in jours[jour].keys():
                    jours[jour][hourDay] = 1
                    jours[jour]['Total'] += 1
                else:
                    jours[jour][hourDay] += 1
                    jours[jour]['Total'] += 1
    # Trie par ordre décroissant du nombre de tentatives par horaire de chaque jour de la periode d'examen
    jours_descending = {}
    jours_descending = OrderedDict(sorted(jours.items(),
                                          key=lambda x: x[1]['Total'], reverse=True))
    for jour in jours_descending.keys():
        temp = OrderedDict(sorted(jours_descending[jour].items(), key=lambda x: x[1], reverse=True))
        jours_descending[jour] = temp
    return json.dumps({
        'horaire ou l_outil a ete le plus utilise pour chaque jour en periode d_examen par ordre decroissant du nbre de tentatives': jours_descending},
        indent=1)


# ___________________________________________________________________Top 5
# 1)	Quel est le jour qui a comptabilité le plus de tentatives ?
def tentativesMaxParJour(essais):
    # Dictionnaire des jours où l'outils a été utilisé
    # et du nombre de tentatatives pour chaque jour  triées par ordre décroissant du nombre de tentatives
    jours = {}
    for essai in essais:
        # Jour de l'essai
        day = essai.date.day
        month = essai.date.month
        year = essai.date.year
        jour = str(day) + "/" + str(month) + "/" + str(year)
        if jour not in jours.keys():
            jours[jour] = 1
        else:
            jours[jour] += 1
    # Jours ou l_outil a ete le plus utilise
    temp = {}
    jourMax = max(jours.items(), key=operator.itemgetter(1))[0]
    temp[jourMax] = jours[jourMax]
    return json.dumps({'Jour ou l_outil a ete le plus utilise': temp}, indent=1)


# 2)	Quel est l’étudiant qui a comptabilisé le plus de tentatives ?
def tentativesMaxParEtudiant(etudiantsDistincts):
    temp = {}
    for etudiant in etudiantsDistincts:
        temp[etudiant.id_etudiant] = etudiant.nbr_essais
    # Etudiant qui a le plus utilise l_outils
    temp2 = {}
    etudiantMax = max(temp.items(), key=operator.itemgetter(1))[0]
    temp2[etudiantMax] = temp[etudiantMax]
    return json.dumps({'Etudiant qui a le plus utilise l_outils': temp2}, indent=1)


# 3)	Quel est l’étudiant qui a comptabilisé le plus de succès ?
# a)	Note: éliminez la multi-validation du même exercice par un étudiant
def succesMaxParEtudiant(etudiantsDistincts):
    temp = {}
    for etudiant in etudiantsDistincts:
        temp[etudiant.id_etudiant] = etudiant.nbr_succes
    # Etudiant qui a comptabilisé le plus de succès
    temp2 = {}
    etudiantMax = max(temp.items(), key=operator.itemgetter(1))[0]
    temp2[etudiantMax] = temp[etudiantMax]
    return json.dumps({'Etudiant qui a comptabilise le plus de succes ': temp2}, indent=1)



# 4)	Quelle est l’erreur de syntaxe la plus courante ?
def couranteSyntaxError(detailsDistincts):
    # Dictionnaire des messages d'erreurs et du nombre d'occurence de chaque erreur
    temp = {}
    for details in detailsDistincts:
        if details.message!="":
            if details.message not in temp.keys():
                temp[details.message] = 1
            else:
                temp[details.message] += 1
    temp2 = {}
    erreurMax = max(temp.items(), key=operator.itemgetter(1))[0]
    temp2[erreurMax] = temp[erreurMax]
    return json.dumps({'Erreur de syntaxe la plus courante et nombre d_occurence': temp2}, indent=1)


# Chargement des données
(exos, groupes, etudiants, essais, details) = dataLoading()

with open("sortie.json", "a") as myfile:
    myfile.write(etudiantsParGroupe(groupes))
    myfile.write(tentativesParGroupe(groupes))
    myfile.write(tentativesParGroupeTries(groupes))
    myfile.write(tentativesMoyensParEtudiant())
    myfile.write(tentativesMoyensParGroupe())
    myfile.write(groupesPlusActifs(groupes))
    myfile.write(exercicesParGroupe(groupes))
    myfile.write(exercicesJamaisReussis(exos))
    myfile.write(tentativesEchecs(exos))
    myfile.write(tentativesParEtudiantSurExoJamaisReussis(exos))
    myfile.write(tempsMoyenReussiteParExo(exos))
    myfile.write(mieuxReussis(exos))
    myfile.write(nombreMeilleursEtudiants(exos))
    myfile.write(picDUtilisationParJourSemaine(essais))
    myfile.write(picDUtilisationParHorraire(essais))
    myfile.write(picHoraireParJourSemaine(essais))
    myfile.write(picDUtilisationEnExamen(essais))
    myfile.write(picHoraireEnExamen(essais))
    myfile.write(tentativesMaxParJour(essais))
    myfile.write(tentativesMaxParEtudiant(etudiants))
    myfile.write(succesMaxParEtudiant(etudiants))
    myfile.write(couranteSyntaxError(details))
