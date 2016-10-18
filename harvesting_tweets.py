# Fecha: Marzo-2016
# Descripcion: Programa que cosecha tweets desde la API de twitter usando tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "a3EFsN0kUu04QtdUJlFdSBrHH"
csecret = "uXXkD81WVnhLk0M8tdNb8jDXAsQhIGzKSFcUQRlDShWFl9Wzg3"
atoken = "2593813213-Fi5yWsk71uKcGmDconMaY8obRVV4A5QXmP9TVQU"
asecret = "4nXx4BNOE9QK5MMW1TxXAxz3U69hBdB1Y1caXp2rJ0Nz0"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            texto = dictTweet["text"] #transformar todo a minúsculas
            if 'ecuador' in texto:
                doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
                print "Guardado " + "=> " + dictTweet["_id"]
            else:
                print 'Ignorado'
        except:
            print "Documento ya existe"
            pass
        return True
    
    def on_error(self, status):
        print status
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('quito')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['quito']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-78.5989,-0.3952,-78.2742,0.1277])  