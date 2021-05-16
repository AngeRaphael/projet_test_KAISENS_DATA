# projet_test_KAISENS_DATA

Collecter des postes (image, texte et commentaires liés aux images) par rapport à un sujet défini sur un réseau social pour les enregistrer dans une base de données MongoDB 


## Ce que fait le code :

Ce script est utilisé pour collecter le texte des messages sur une page Instagram ayant fait un poste relatif à sujet définie, récupère également les informations relatives aux comptes du propriétaires de la page et du message posté tels que l’image ou la vidéo posté, le nombre de commentaires, les commentaires et leurs réponses, le nom et l’identifiant du compte Instagram de chaque utilisateur ayant faire un commentaire est également recueillir. Et ces informations sont enregistrées dans une base de données MongoDB stocke également le lien vers le profil de la personne qui a fait le commentaire.

## Comment collecte-t-il les informations :

Premièrement, le scripte récupère le sujet dont l’on cherche les postes et commentaires, ensuite le code établit une recherche sur google de façon automatisée en ajoutant au thème renseigné le mot clé « Instagram » afin d’obtenir les pages ayants fait un poste sur ce thème. Ensuite un filtre est effectué pour récupérer uniquement les liens qui rediriges vers un poste Instagram. Une fois les liens collectés, une conversion des pages Instagram en formats JSON nous permet de naviguer et recueillir tout ceux dont nous avons besoins. Pour finir nous les stockons dans une base de données MongoDB, le code crée également deux dossiers l’une pour stocker les images et l’autres pour les vidéos postés.

### Attention !!! :

L’utilisation de collection de données sur Instagram ou Facebook via Bot sans permission est illégales, donc plusieurs requêtes (environs 10) successives de collectes d’information excessive déclenches un captcha non pris en compte par ce code. 

Sources d’information : 

https://www.facebook.com/robots.txt 

https://www.instagram.com/robots.txt


### Solution Proposée par l'Auteur : 
#### Une solution serait de changer de point d’accès internet en utilisant par exemple une connexion partagé par un terminal mobile. Ceci changera votre adresse réseau de connexion et donc considéré comme un nouveau internaute.

