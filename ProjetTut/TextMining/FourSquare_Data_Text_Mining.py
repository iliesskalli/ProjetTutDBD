
#Importation des packages requis :
#region
from scipy.integrate import quad
from geopy.geocoders import Nominatim

import json                         #Exploration des données
import requests                     #Requêtage de l'application
import os                           #Fonctions de base de python
import pandas as pd                 #Utilisations des Dataframes
import datetime                     #Utilisations du Datetime pour now()
import scipy.stats                  #Utilisation de la courbe de Gauss
import numpy as np      


from collections import Counter     #conteur
from string import punctuation      #Pour éviter d'avoir des ponctuation dans les mots fréquents


import seaborn as sns               #module pour le graph
import matplotlib.pyplot as plt     #"Idem"
import nltk
import qwant                        #importation de qwant (pip install qwant)
#import spacy                       #Utilisation du framework spacy pour la fréquence
#nlp = spacy.load("en_core_web_lg")
from stop_words import get_stop_words #Liste de mots banaux




                                        ###############################################################################
                                        #                                                                             #
                                        #                                                                             #
                                        #                                                                             #
                                        #                              API Foursquare                                 #
                                        #                                                                             #
                                        #                                                                             #
                                        #                                                                             #
                                        ###############################################################################





#endregion

#Url de connexion à l'API
url = 'https://api.foursquare.com/v2/venues/explore'

#Permet d'utiliser le temps dans le programme
current_time = datetime.datetime.now()

#On affiches toutes les lignes de dataframes pour éviter les raccourcis : 
pd.set_option('display.max_rows', 500)

#Paramétrage de l'API :
#region
#   # # # # # # # # # # # # # # # # # # # # # #
#Définition du paramétrage de l'API #
#Entrée : Latittude et Longitude : Int #
#Paramètres : l'ID Client (Qui utilise l'API) : String #
#           - Mot de Passe du client : String #
#           - La date d'actualisation : DateTime #
#           - Les coordonées GPS : String #
#           - La demande : String # #
#Sortie : Les Paramètres de l'API #
#Description : Permet de requêter Foursquare avec toutes les données
#necessaires #
#   # # # # # # # # # # # # # # # # # # # # # #
def customParams(latitude, longitude, besoin):
    #Si le mois est inférieur à 10, on rajoute un "0" dans la date pour être
    #conforme à la norme foursquare
    if int(current_time.month) < 10 :
        params = dict(client_id='NCY3QDJ2ZNXNNQNQVQBVLQO44JBMGTYL3KQSHQBT3WFVIOPW',
        client_secret='R3CCH5GJHTAS3IAQUV1H2X5NJT20TNTIJDW5QXMBEYMSUW35',

        v = str(current_time.year) + str(0) + str(current_time.month) + str(current_time.day),

        #Paramètres entrés par l'utilisateurs
        ll= str(latitude) + ',' + str(longitude),
        query='coffee',
    
        #Limite de données
        limit=75)
        return params
    else :
        params = dict(client_id='NCY3QDJ2ZNXNNQNQVQBVLQO44JBMGTYL3KQSHQBT3WFVIOPW',
        client_secret='R3CCH5GJHTAS3IAQUV1H2X5NJT20TNTIJDW5QXMBEYMSUW35',

        v = str(current_time.year) + str(current_time.month) + str(current_time.day),

        #Paramètres entrés par l'utilisateurs
        ll= str(latitude) + ',' + str(longitude),
        query=besoin,
    
        #Limitation du nombre de données
        limit=10)
        return params
#endregion
#Identification pour géolocaliser la ville
geolocator = Nominatim(user_agent = "lfptmathieufr@outlook.fr")
def city_state_country(coord):
    location = geolocator.reverse(coord, timeout = 5, exactly_one=True,)
    #print(location.raw)
    #time.sleep(10)
    address = location.raw['address']
    city = address.get('city', '')
    village = address.get('village', '')
    municipality = address.get('municipality', '')
    state = address.get('state', '')
    country = address.get('country', '')
    #print (city, municipality, village)
    if((municipality == "") or (municipality == None)):
        return city
    elif((village == "") or (village == None)):
        return municipality
    else :
        return village

#Création de la fonctio orgaData :
def orgaData(latitude, longitude, besoin) :
    #Requetage de l'API : Donnees Authentiques
    resp = requests.get(url=url, params=customParams(latitude, longitude, besoin))
    data = json.loads(resp.text)

    #Variable de tri de la donnée
    groups = data['response']['groups']
    groupSize = len(groups)
    counteraddr = 0
    counter = 0

    #Création du tableau de données :
    dfAuth = pd.DataFrame({"Nom":[], "Adresse":[], "Ville":[], "Coordonees GPS":[], "Priorité" :[]})

    #Peuplement du tableau :
    #~Parcours de la donnée :
    #~~Parcours des groupes
    for index in range(groupSize):
        group = groups[index]
        items = group['items']
        itemsSize = len(items)

    #~~Parcours de la range
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

        #Établissement de la priorité : On utilisera une loi normale de type Gauss : 
        x_min = 8.0
        x_max = 16.0

        mean = 8.0 
        std = 2.0

        x = np.linspace(x_min, x_max, itemsSize)
        np.size(x)

        Gauss = scipy.stats.norm.pdf(x,mean,std)*500

        latlong= str(latitude) + ', ' + str(longitude)
        city = city_state_country(latlong)
        
        dfTemp = pd.DataFrame({"Nom": [venueName], "Adresse": [address], "Ville":[city], "Coordonees GPS": [str(lat) + ", " + str(lng)], "Priorité": [Gauss[i]]})
        dfAuth = dfAuth.append(dfTemp, ignore_index=True)
        dfTemp = None 
    return dfAuth

#Paramètres manuels :
latitude = 48.8534
longitude = 2.3488

print("Obtention des données...")
#Lieu Recherché Authentique
print("     > Locales ..................................................")
df0 = orgaData(latitude, longitude, "restaurants")
print("     > Locales .................................................. : OK")

#Échantillonage sur 30km
#~Échantillon Nord
print("     > Echantillon Nord .........................................")
df1 = orgaData(latitude + 0.25, longitude, "restaurants")
print("     > Echantillon Nord ......................................... : OK")


#~Échantillon Sud Est
print("     > Echantillon Sud-Est ......................................")
df2 = orgaData(latitude - 0.2, longitude + 0.2, "restaurants")
print("     > Echantillon Sud-Est ...................................... : OK")

#~Échantillon Sud Ouest
print("     > Echantillon Sud-Ouest ....................................")
df3 = orgaData(latitude - 0.2, longitude - 0.2, "restaurants")
print("     > Echantillon Sud-Ouest .................................... : OK")

#Échantillonage sur 60km
#~Échantillon Sud
print("     > Echantillon Sud+ .........................................")
df4 = orgaData(latitude - 0.55 , longitude, "restaurants")
print("     > Echantillon Sud+ ......................................... : OK")

#~Échantillon Nord-Est
print("     > Echantillon Nord-Est+ ....................................")
df5 = orgaData(latitude + 0.5, longitude + 0.5, "restaurants")
print("     > Echantillon Nord-Est+ .................................... : OK")

#~Échantillon Nord-Ouest
print("     > Echantillon Nord-Ouest+ ..................................")
df6 = orgaData(latitude + 0.5, longitude - 0.5, "restaurants")
print("     > Echantillon Nord-Ouest+ .................................. : OK")

#Affichage : 
print ("Données locales :\n")
print(df0)
print("\n-------------------------------------------------------------")
print ("Données échantillonés N°1 (Restaurants) :\n")
print(df1)
print("\n-------------------------------------------------------------")
print ("Données échantillonés N°2 (Restaurants) :\n")
print(df2)
print("\n-------------------------------------------------------------")
print ("Données échantillonés N°3 (Restaurants) :\n")
print(df3)
print("\n-------------------------------------------------------------")
print ("Données échantillonés N°4 (Restaurants) :\n")
print(df4)
print("\n-------------------------------------------------------------")
print ("Données échantillonés N°5 (Restaurants) :\n")
print(df5)
print("\n-------------------------------------------------------------")
print ("Données échantillonés N°6 (Restaurants) :\n")
print(df6)







                                        ###############################################################################
                                        #                                                                             #
                                        #                                                                             #
                                        #                                                                             #
                                        #                              Text Mining                                    #
                                        #                                                                             #
                                        #                                                                             #
                                        #                                                                             #
                                        ###############################################################################




#Récupération de la ville
ville = df0.loc[0,"Ville"]
##### récupération et duplication des données locales ####
#(On peut aussi le faire avec une boucle)

pon0 = (df0.loc[0,"Nom"] + ' '+ df0.loc[0,"Adresse"] + ' ') * int(round(df0.loc[0,"Priorité"]))
pon1 = (df0.loc[1,"Nom"] + ' '+ df0.loc[1,"Adresse"] + ' ') * int(round(df0.loc[1,"Priorité"]))
pon2 = (df0.loc[2,"Nom"] + ' '+ df0.loc[2,"Adresse"] + ' ') * int(round(df0.loc[2,"Priorité"]))
pon3 = (df0.loc[3,"Nom"] + ' '+ df0.loc[3,"Adresse"] + ' ') * int(round(df0.loc[3,"Priorité"]))
pon4 = (df0.loc[4,"Nom"] + ' '+ df0.loc[4,"Adresse"] + ' ') * int(round(df0.loc[4,"Priorité"]))
pon5 = (df0.loc[5,"Nom"] + ' '+ df0.loc[5,"Adresse"] + ' ') * int(round(df0.loc[5,"Priorité"]))
pon6 = (df0.loc[6,"Nom"] + ' '+ df0.loc[6,"Adresse"] + ' ') * int(round(df0.loc[6,"Priorité"]))
pon7 = (df0.loc[7,"Nom"] + ' '+ df0.loc[7,"Adresse"] + ' ') * int(round(df0.loc[7,"Priorité"]))
pon8 = (df0.loc[8,"Nom"] + ' '+ df0.loc[8,"Adresse"] + ' ') * int(round(df0.loc[8,"Priorité"]))
pon9 = (df0.loc[9,"Nom"] + ' '+ df0.loc[9,"Adresse"] + ' ') * int(round(df0.loc[9,"Priorité"]))
pon10 = (df0.loc[10,"Nom"] + ' '+ df0.loc[10,"Adresse"] + ' ') * int(round(df0.loc[10,"Priorité"]))
pon11 = (df0.loc[11,"Nom"] + ' '+ df0.loc[11,"Adresse"] + ' ') * int(round(df0.loc[11,"Priorité"]))
pon12 = (df0.loc[12,"Nom"] + ' '+ df0.loc[12,"Adresse"] + ' ') * int(round(df0.loc[12,"Priorité"]))
pon13 = (df0.loc[13,"Nom"] + ' '+ df0.loc[13,"Adresse"] + ' ') * int(round(df0.loc[13,"Priorité"]))

ponlocal = pon0+pon1+pon2+pon3+pon4+pon5+pon6+pon7+pon8+pon9+pon10+pon11+pon12+pon13

####### Nettoyage des données locaux ########

ponlocal = ponlocal.lower()                                # Tout mettre en minuscule
ponlocal = ''.join(c for c in ponlocal if not c.isdigit()) # Enlève les nombre
ponlocal = ponlocal.split()                                # Hacher en liste de mots

# Dictionnaire perso, mots communs 
stopwords1 = set(["ai","avais","a","as","avons","est","etait","ete","la","j","d","l",
"peu","en","ce","au","vu","faire","pour","une","nan","de","et","nous","que","si","le","il","ma","vous","y","c","des","on","un","les","je","ne","pas","ces","m","qu","fallut","ou","sur","du","fais","me","fait","fur","mais","cela","pr","avait","mis","plus","tous","part","sinon","tout","sont","sans","an","qui","cest","cas","par","memes","meme",
"sous","aurais","malgre","etaient","vraiment","donc","votre","plutot","passe","rn","&",
"n","avoir","aussi","chose","assez","trop","moins","mieux","beaucoup","grace","cette","vrai","voir","choses","trouve","journee","appris","pense","bien","bonjour","a.","2","3","4","6","7"])

#(mots banaux de la langue française)
stopwordsfr = get_stop_words('fr')
#(mots banaux de la langue anglaise)
stopwordsen = get_stop_words('en')

stopwords = set(stopwordsfr)|set(stopwords1)|set(stopwordsen) #fusion des listes de stopwords

#Supprime les mots banaux
for h1 in ponlocal:
        
    for h2 in stopwords:
        if h2 == h1:
            ponlocal.remove(h1)              

#Pour un nettoyage complet 
"""
import string # pour charger une librairie de ponctuation (string.punctuation)
import unicodedata # pour remplacer tous les caractères accentués
#corpus = df1.iloc[:,1]
for i in range(len(ponlocal)) :
    tmp = str(ponlocal[i])
    tmp = tmp.lower() # Supprimer les majuscules
    tmp = tmp.replace("'"," ") # Remplacer apostrophe par une espace
    #tmp = tmp.replace("\n"," ") # Supprimer les retours chariot
    tmp = tmp.translate(str.maketrans("","", string.punctuation)) # Supprimer la ponctuation
    tmp = tmp.encode('utf-8').decode('utf-8') # Éliminations des caractères spéciaux et accentués
    tmp = unicodedata.normalize('NFD', tmp).encode('ascii', 'ignore')   
    
    #ponlocal[i] = tmp
"""    

#fréquence
mots_lieux = [(x[0]) for x in Counter(ponlocal).most_common(50)]     #récupère les 50 mots les plus fréquents 

print("\n-------------------------------------------------------------")
print("Les Mots locaux les plus fréquents :")
print(mots_lieux)

### Même processus pour les autres lieux ### 

#récupération et duplication des données échantillonés N°1

pon0 = (df1.loc[0,"Nom"] + ' '+ df1.loc[0,"Adresse"] + ' ') * int(round(df1.loc[0,"Priorité"]))
pon1 = (df1.loc[1,"Nom"] + ' '+ df1.loc[1,"Adresse"] + ' ') * int(round(df1.loc[1,"Priorité"]))
pon2 = (df1.loc[2,"Nom"] + ' '+ df1.loc[2,"Adresse"] + ' ') * int(round(df1.loc[2,"Priorité"]))
pon3 = (df1.loc[3,"Nom"] + ' '+ df1.loc[3,"Adresse"] + ' ') * int(round(df1.loc[3,"Priorité"]))
pon4 = (df1.loc[4,"Nom"] + ' '+ df1.loc[4,"Adresse"] + ' ') * int(round(df1.loc[4,"Priorité"]))

ponechan1 = pon0+pon1+pon2+pon3+pon4

 

#récupération et duplication des données échantillonés N°2

pon0 = (df2.loc[0,"Nom"] + ' '+ df2.loc[0,"Adresse"] + ' ') * int(round(df2.loc[0,"Priorité"]))
pon1 = (df2.loc[1,"Nom"] + ' '+ df2.loc[1,"Adresse"] + ' ') * int(round(df2.loc[1,"Priorité"]))
pon2 = (df2.loc[2,"Nom"] + ' '+ df2.loc[2,"Adresse"] + ' ') * int(round(df2.loc[2,"Priorité"]))
pon3 = (df2.loc[3,"Nom"] + ' '+ df2.loc[3,"Adresse"] + ' ') * int(round(df2.loc[3,"Priorité"]))
pon4 = (df2.loc[4,"Nom"] + ' '+ df2.loc[4,"Adresse"] + ' ') * int(round(df2.loc[4,"Priorité"]))

ponechan2 = pon0+pon1+pon2+pon3+pon4



#récupération et duplication des données échantillonés N°3

pon0 = (df3.loc[0,"Nom"] + ' '+ df3.loc[0,"Adresse"] + ' ') * int(round(df3.loc[0,"Priorité"]))
pon1 = (df3.loc[1,"Nom"] + ' '+ df3.loc[1,"Adresse"] + ' ') * int(round(df3.loc[1,"Priorité"]))
pon2 = (df3.loc[2,"Nom"] + ' '+ df3.loc[2,"Adresse"] + ' ') * int(round(df3.loc[2,"Priorité"]))
pon3 = (df3.loc[3,"Nom"] + ' '+ df3.loc[3,"Adresse"] + ' ') * int(round(df3.loc[3,"Priorité"]))
pon4 = (df3.loc[4,"Nom"] + ' '+ df3.loc[4,"Adresse"] + ' ') * int(round(df3.loc[4,"Priorité"]))


ponechan3 = pon0+pon1+pon2+pon3+pon4




#récupération et duplication des données échantillonés N°4

pon0 = (df4.loc[0,"Nom"] + ' '+ df4.loc[0,"Adresse"] + ' ') * int(round(df4.loc[0,"Priorité"]))
pon1 = (df4.loc[1,"Nom"] + ' '+ df4.loc[1,"Adresse"] + ' ') * int(round(df4.loc[1,"Priorité"]))
pon2 = (df4.loc[2,"Nom"] + ' '+ df4.loc[2,"Adresse"] + ' ') * int(round(df4.loc[2,"Priorité"]))

ponechan4 = pon0+pon1+pon2



#récupération et duplication des données échantillonés N°5

pon0 = (df5.loc[0,"Nom"] + ' '+ df5.loc[0,"Adresse"] + ' ') * int(round(df5.loc[0,"Priorité"]))
pon1 = (df5.loc[1,"Nom"] + ' '+ df5.loc[1,"Adresse"] + ' ') * int(round(df5.loc[1,"Priorité"]))
pon2 = (df5.loc[2,"Nom"] + ' '+ df5.loc[2,"Adresse"] + ' ') * int(round(df5.loc[2,"Priorité"]))
pon3 = (df5.loc[3,"Nom"] + ' '+ df5.loc[3,"Adresse"] + ' ') * int(round(df5.loc[3,"Priorité"]))
pon4 = (df5.loc[4,"Nom"] + ' '+ df5.loc[4,"Adresse"] + ' ') * int(round(df5.loc[4,"Priorité"]))


ponechan5 = pon0+pon1+pon2+pon3+pon4



#récupération et duplication des données échantillonés N°6

pon0 = (df6.loc[0,"Nom"] + ' '+ df6.loc[0,"Adresse"] + ' ') * int(round(df6.loc[0,"Priorité"]))
pon1 = (df6.loc[1,"Nom"] + ' '+ df6.loc[1,"Adresse"] + ' ') * int(round(df6.loc[1,"Priorité"]))
pon2 = (df6.loc[2,"Nom"] + ' '+ df6.loc[2,"Adresse"] + ' ') * int(round(df6.loc[2,"Priorité"]))
pon3 = (df6.loc[3,"Nom"] + ' '+ df6.loc[3,"Adresse"] + ' ') * int(round(df6.loc[3,"Priorité"]))
pon4 = (df6.loc[4,"Nom"] + ' '+ df6.loc[4,"Adresse"] + ' ') * int(round(df6.loc[4,"Priorité"]))


ponechan6 = pon0+pon1+pon2+pon3+pon4

#Récupération de tous les mots échantillonés
mots_echants = ponechan1+ponechan2+ponechan3+ponechan4+ponechan5+ponechan6   

####### Nettoyage des mots échantillonés ########
mots_echants = mots_echants.lower() 
mots_echants = mots_echants.split()



#Supprime les mots banaux
for h1 in mots_echants:
        
    for h2 in stopwords:
        if h2 == h1:
            mots_echants.remove(h1)  


#fréquence
mots_echantst = [(x[0]) for x in Counter(mots_echants).most_common(500)]      #récupère les 350 mots les plus fréquents 
            


#Le total des mots échantillonés
  
print("\n-------------------------------------------------------------")
print("Les mots des autres Lieux: \n")
print(mots_echantst)                                                        



####### Comparaisons Mots du lieux avec les mots échantillonés ######
                                                                            #http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/td2a_eco_NLP_tf_idf_ngrams_LDA_word2vec_sur_des_extraits_litteraires.html#frequence-dun-mot
                                                                            #http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/td2a_Seance_7_Analyse_de_textes.html

print("\n-------------------------------------------------------------")
print("Confrontation / Comparaison: \n")

#création dataframe avec les mots du lieux et leurs scrore de proximité 
txt = nltk.TextCollection(mots_lieux) 
dfms = pd.DataFrame(columns = ['score'])
dfms.insert(0,'mots',mots_lieux)      


#calcul du score de proximité de chaque mots locaux avec les mots des autres lieux avec le module nltk.tf_idf
#plus le scrore est élevé, plus le mot local est proche des mots des autres lieux.
for index, row in dfms.iterrows():
    dfms.loc[index, 'score'] = txt.tf_idf(row['mots'],mots_echantst) 

#Tri
dfms = dfms.sort_values(by = 'score')

print("\n-------------------------------------------------------------")
print("\n-------------------------------------------------------------")
print("Mots du Lieu et leurs score: \n")
print(dfms)



###### Récupération des sites locaux avec l'API du moteur de recherche  qwant #####

#Récupération des mots avec un score = 0
# Ces mots sont des mots spécifiques du lieux

dfmscore0 = dfms.loc[ dfms['score']==0,]


motscore0 = ""
for x in dfmscore0['mots'][0:3] :           
    motscore0 = motscore0 + ' ' + x

print("\n-------------------------------------------------------------")
print("Mots spécifiques du lieu: \n")
print(motscore0)

#ici, la recherche se fera avec les mots clés du lieux (score = 0)
#var_1 = qwant.items("iut perigueux")                         # var_1 contient le résultat de la recherche 

var_2 = qwant.items(motscore0+' '+ville)[1]['url']    # Pour récupérer seulement les urls
var_3 = qwant.items(motscore0+' '+ville)[2]['url'] 
var_4 = qwant.items(motscore0+' '+ville)[3]['url']
var_5 = qwant.items(motscore0+' '+ville)[4]['url'] 

print(var_2)                                                  # Affiche le résultat de la recherche
print(var_3) 
print(var_4)
print(var_5)



                                                #####                   ####
                                                #   Ce qui reste à faire   #
                                                #####                   ####     

#### Webscrapping ####


##### Récupération du contenu des sites en webscrapping avec BeautifulSoup #####
#--> voir l'exemple dans le dossier webscrapping (remplacer l'url par les urls obtenu précédemment)

#### Ensuite, récupérer les mots les plus fréquent  des pages scrapper (penser à enlever les mots communs) ####
#--> voir méthode utiliser plus haut pour avoir les mots fréquent

#### Enfin croiser les mots clés du lieux avec les mots fréquent des pages scrapper pour obtenir une page web spécifique au lieux ####


