#Importations des libraries
import json
import requests
import os
import pandas as pd

#Url de connexion à l'API
url = 'https://api.foursquare.com/v2/venues/explore'

def customParams(latitude, longitude):
    params = dict(client_id='NCY3QDJ2ZNXNNQNQVQBVLQO44JBMGTYL3KQSHQBT3WFVIOPW',
    client_secret='R3CCH5GJHTAS3IAQUV1H2X5NJT20TNTIJDW5QXMBEYMSUW35',

    #Variables de localisation :
    lattitude = 5,
    longitude = 5,

    #Paramètres entrés par l'utilisateurs
    #v='20200323',
    ll= str(latitude) + ',' + str(longitude),
    query='restaurants',
    
    #Limite de données
    limit=75)
    return params
#Requêtage du serveur
print("Connexion au serveur")

#region Requêtage Initial

#Identifiants de l'API
#params = dict(
#    client_id='NCY3QDJ2ZNXNNQNQVQBVLQO44JBMGTYL3KQSHQBT3WFVIOPW',
#    client_secret='R3CCH5GJHTAS3IAQUV1H2X5NJT20TNTIJDW5QXMBEYMSUW35',

#    #Variables de localisation :
#    lattitude = 5,
#    longitude = 5,

#    #Paramètres entrés par l'utilisateurs
#    v='20180323',
#    ll='44.837789,-0.57918',
#    query='restaurants',
    
#    #Limite de données
#    limit=75)

#endregion
print("Récupération des données")
print("\n-------------------------------------------------------------")

#Requetage de l'API : Donnees Authentiques
resp = requests.get(url=url, params=customParams(45.1833, 0.7167))
data = json.loads(resp.text)

#Tri des données dans la catégorie
##################################
#
#Response
    #
    #Groups
##################################
groups = data['response']['groups']
groupSize = len(groups)
counteraddr = 0
counter = 0

dfAuth = pd.DataFrame({"Nom":[], "Adresse":[], "Coordonees GPS":[]})
# Parcours des groupes
for index in range(groupSize):
    group = groups[index]
    items = group['items']
    itemsSize = len(items)

# Parcours de la range
    for i in range(itemsSize):
        counter+=1
        venue = items[i]['venue']
        venueName = venue['name']           #Récupération du nom
        location = venue['location']        #Récupération de la location
        address = ''
        try:
            address = location['address']   #Récupération de l'adresse si elle existe
        except KeyError:
            address = 'None'            
            counteraddr+=1
        lng = location['lng']               #Récupération de la longitude
        lat = location['lat']               #Récupération de la latittude
        
        #Affichage des valeurs.
        print("Name = " + venueName)
        print("Adresse = " + address)
        print("Longitude=" + str(lng))
        print("Latitude=" + str(lat))
        print("\n-------------------------------------------------------------")
        print("Enregistrement des données...")
        dfTemp = pd.DataFrame({"Nom": [venueName], "Adresse": [address], "Coordonees GPS": [str(lat) + ", " + str(lng)]})
        dfAuth = dfAuth.append(dfTemp, ignore_index=True)
        dfTemp = None 
        print("\n-------------------------------------------------------------")
print("Nombre d'adresses inexistantes : " + str(counteraddr))
print("Nombre de résultats : " + str(counter))
print("\n-------------------------------------------------------------")
print(dfAuth)
print("\nDonnées Sauvegardés !")
print("\n-------------------------------------------------------------")
print("Deuxième Récupération de données :")
print("\n-------------------------------------------------------------")
 
print("Récupération des données")
print("\n-------------------------------------------------------------")

#Requetage de l'API : Donnees Authentiques
resp = requests.get(url=url, params=customParams(45.6833, 0.7167))
data = json.loads(resp.text)

#Tri des données dans la catégorie
##################################
#
#Response
    #
    #Groups
##################################
groups = data['response']['groups']
groupSize = len(groups)
counteraddr = 0
counter = 0

dfNord = pd.DataFrame({"Nom":[], "Adresse":[], "Coordonees GPS":[]})
# Parcours des groupes
for index in range(groupSize):
    group = groups[index]
    items = group['items']
    itemsSize = len(items)

# Parcours de la range
    for i in range(itemsSize):
        counter+=1
        venue = items[i]['venue']
        venueName = venue['name']           #Récupération du nom
        location = venue['location']        #Récupération de la location
        address = ''
        try:
            address = location['address']   #Récupération de l'adresse si elle existe
        except KeyError:
            address = 'None'            
            counteraddr+=1
        lng = location['lng']               #Récupération de la longitude
        lat = location['lat']               #Récupération de la latittude
        
        #Affichage des valeurs.
        print("Name = " + venueName)
        print("Adresse = " + address)
        print("Longitude=" + str(lng))
        print("Latitude=" + str(lat))
        print("\n-------------------------------------------------------------")
        print("Enregistrement des données...")
        dfTemp = pd.DataFrame({"Nom": [venueName], "Adresse": [address], "Coordonees GPS": [str(lat) + ", " + str(lng)]})
        dfNord = dfNord.append(dfTemp, ignore_index=True)
        dfTemp = None 
        print("\n-------------------------------------------------------------")
print("Nombre d'adresses inexistantes : " + str(counteraddr))
print("Nombre de résultats : " + str(counter))
print("\n-------------------------------------------------------------")
print(dfNord)
print("\nDonnées Sauvegardés !")
print("\n-------------------------------------------------------------")
print("Deuxième Récupération de données :")
#print(groups)
#os.chdir("C:/Users/automaticien/Desktop/Mathieu/Projets tutorés")
#os.chdir("C:/")
#print("Génération du fichier")
#file = open("data.json", "w")
#file.write(resp.text)
#file.close()
#print("Fermeture du fichier\n\n")