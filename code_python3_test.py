#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, sys, webbrowser

from bs4 import BeautifulSoup

import urllib

import time, os

from pymongo import MongoClient

from bson.objectid import ObjectId


# In[2]:


#connexion à MongoDB
    
server = '127.0.0.1'

port = 27017

dbName = 'Data_Test_KAISENS'

client = MongoClient(server,port)

db = client[dbName]

postes_BD = db["postes"]

commentaires_BD = db["commentaires"]



postes = { "_id" : None, "page_url" : None, "message_poste" : None, "nbre_commentaire" : None , "url_video" : None , "url_image" : None , "infos_poste" : None , "owner_name" : None , "owner_compte" : None}

commentaires = { "_id" : None, "page_url" : None , "owner_compte_commentaire" : None , "commentaire" : None }



# In[3]:


def liens_postes_sujet(sujet):
    
    
    pages_instagram_recupere = []

    topic = sujet + " instagram"
    
    reseau_social = "www.instagram.com"

    topic_conv = urllib.parse.quote(topic, safe='')

    url_search = "http://www.google.com/search?q=" + topic_conv
    
    #uniquement pour la page instagramme, le cas de notre exemple
    id_page_instagram = 12

    print(url_search) 

    try:
        
        resultats = requests.get(url_search)

        resultats.raise_for_status()
        
        
        if resultats.ok:

            soup = BeautifulSoup(resultats.text, 'lxml')

            liens_pages_instagram = soup.find_all('a')

            for i in range(len(liens_pages_instagram)):

                if reseau_social in liens_pages_instagram[i]['href']:
                    
                    
                    if liens_pages_instagram[i]['href'].count('/p/') > 0: 

                        start = liens_pages_instagram[i]['href'].index('https') 
                        
                        #3 pour prendre en compte le nombre de caractere de /p/
                        end =   liens_pages_instagram[i]['href'].index('/p/') + 3 + id_page_instagram

                        lien = liens_pages_instagram[i]['href'][start: end]

                        pages_instagram_recupere.append(lien)

                    
            if len(pages_instagram_recupere) == 0 :
                
                print('Aucune reference sur instagram se trouvant sur Google')

            print(pages_instagram_recupere)  

        else:

            print("Erreur de la recherche: Erreur : " + resultats.text )

        
    except Exception as e:
                
        print(e)
            
        exit()
        
    return pages_instagram_recupere


# In[4]:


def collection_posts(liens_post):
    
    try:
        
        if not (os.path.exists('Dossier_videos_post') and os.path.exists('Dossier_images_post')):

            os.makedirs('Dossier_videos_post')

            os.makedirs('Dossier_images_post')


        posts = []

        path = os. getcwd()

        posts = liens_post

        for post in posts:

            headers = {'User-Agent': 'Mozilla'}

            r = requests.get('{}?__a=1'.format(post), headers=headers)

            print(r)

            if r.ok:

                data = r.json()['graphql']['shortcode_media']

                shortcode = data['shortcode']

                is_video = data['is_video']



                #recupération des informations du postes    

                if is_video:

                    url_videos_post = data['video_url']

                    #Téléchargment de la vidéo et stocker
                    urllib.request.urlretrieve(url_videos_post, 'Dossier_videos_post/{}.mp4'.format(shortcode))

                    #Insertion dans le dictionnaire
                    postes["url_video"] =  path + '/Dossier_videos_post/{}.mp4'.format(shortcode)


                else:

                    url_images_post = data['display_url']

                    #Téléchargment de l'imge et stocker
                    urllib.request.urlretrieve(url_images_post, 'Dossier_images_post/{}.jpg'.format(shortcode))

                    #Insertion dans le dictionnaire
                    postes["url_image"] =  path + '/Dossier_images_post/{}.jpg'.format(shortcode)

                if len(data['accessibility_caption']) < 40:
                    
                    infos_post = data['accessibility_caption'].text

                    infos_post = str(infos_post)[0:str(infos_post).index('.')+1]
                
                message_post = data['edge_media_to_caption']['edges'][0]['node']['text']

                commentaires_post = data['edge_media_to_parent_comment']['edges']

                nombre_commentaires = len(commentaires_post)

                infos_owner_compte = data['owner']['username']

                infos_owner_fulName = data['owner']['full_name']



                #Insertion dans le dictionnaire
                postes["_id"] = ObjectId() 
                postes["page_url"] =  post
                postes["message_poste"] = message_post
                postes["nbre_commentaire"] = nombre_commentaires
                postes["infos_poste"] = infos_post
                postes["owner_name"] =  infos_owner_fulName
                postes["owner_compte"] = infos_owner_compte

                #INSERTION DANS LA BD MONGO
                InsertedResultObj = postes_BD.insert_one(postes)   


                #affichages des information collectées

                print('++++++++++++++++ Infos propriétaire du compte ++++++++++++++++++++++++++++')

                print('ID compte: '+ str(infos_owner_compte))

                print('Nom du propriétaire du compte: '+ str(infos_owner_fulName))

                print('Information sur le poste: '+ str(infos_post))

                print('Nombre de commentaire: ' + str(nombre_commentaires))

                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


                print('============================Message du post===============================')

                print(message_post)

                print('')


                print('Nombre de commentaire: ' + str(nombre_commentaires))

                print('==========================================================================')

                for p in range(nombre_commentaires):


                    contenu_msg_poster = commentaires_post[p]['node']['text']
                    owner_commentaire = commentaires_post[p]['node']['owner']['username']



                    #Insertion dans le dictionnaire
                    commentaires["_id"] = ObjectId() 
                    commentaires["page_url"] = post
                    commentaires["owner_compte_commentaire"] =  owner_commentaire
                    commentaires["commentaire"] = contenu_msg_poster



                    #INSERTION DANS LA BD MONGO
                    InsertedResultObj = commentaires_BD.insert_one(commentaires)




                    print(str(p)+ ' ' +str(owner_commentaire)+'------Commentaires du post---------') 

                    print(contenu_msg_poster)

                    print('-----------------------------------------------------------------------')


            else:

                print('Warning : probleme de connexion')

       
    
    except:
        
        print("Erreur de traitement: Trop de requettes sans authentification")
        
        exit()
    
    print('Fin')


# In[5]:


def main():
    
    #---------examples de topic--------#
    
    #décès de jacques chirac
    #Election Emmanuel Macron
    #Concert de Maitre Gims au stade de france

    
    #----------------------------------#

    
    topic = "Election Emmanuel Macron"  
    
    liens = liens_postes_sujet(topic)
    
    collection_posts(liens)
    
    print('---Programme terminé---')
        


# In[6]:


if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:




