#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON

ckey = "Lz3BzqoqPJA7hrLE7XnYOncdH"
csecret = "1MRn8ElY8Ea24HBSXCvIrVTR0rx3vWA8WFOgEtaTH8SfBQ4uY1"
atoken = "742503304056459264-a8gYllNQEpKAP3O8f73cUgUcoyIdZ0D"
asecret = "LO4oZ55UiXWBlFPuvub78TcDt1vTjAzNYaOecOMMXoK6q"


class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('prueba3')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['prueba3']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(locations=[-78.519583,-0.228567,-78.480944,-0.19247])
twitterStream.filter(track = ["ecuador", "lol", "darius"])