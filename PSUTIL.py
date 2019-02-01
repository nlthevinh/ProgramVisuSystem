import psutil
import requests
import simplejson as json

########## Définition des variables ##############
CPU= psutil.cpu_percent()
#
DISK=psutil.disk_usage('/')[3]

host=psutil.net_if_addrs()

RAMT=psutil.virtual_memory()[0]
RAMU=psutil.virtual_memory()[3]

verifRequete="";

headers = {"Content-Type" : "application/json"}

############## Recherche de l'adresse IP ####################
for k, v in host.items():
    IP = v[0].address


#################### Stockage des octets reçus depuis le début de la connexion ##############
NETWORK=psutil.net_io_counters(pernic=True)
key=list(NETWORK.keys())[:-1][0]
NETWORK=NETWORK[key].bytes_recv



####################### Envoie des données sous format JSON ###############
payload = {'IP':IP,'CPU':CPU,'DISK':DISK,'NET':NETWORK,'RAMT':RAMT,'RAMU':RAMU}
data = json.dumps(payload)

##############################  Envoie de la requete ###################################
try:
    r = requests.post("http://192.168.3.55:5000/collect2", data=json.dumps(data),headers=headers)
    print(r.content)

################## Vérfication de la connexion #####################
    if r.status_code == 200:
        print("Code 200, connexion réussie !")
    elif r.status_code == 404:
        print("!!!!!! Code  404 !!!!!!!!")
    elif r.status_code == 405:
        print("!!!!!! Code  405 !!!!!!!!")
    elif r.status_code == 500:
        print("!!!!!!! Code de 500 !!!!!!")
except:
    print("Erreur lors de la connexion")
