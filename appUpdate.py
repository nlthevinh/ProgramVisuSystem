#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request
import pymysql
import json

app = Flask(__name__)

class Database:
    def __init__(self):
        host = "192.168.3.97"
        user = "test"
        password = "123"
        db = "base"
        connection = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit = True)
        self.cursor = connection.cursor()

    def update(self, data):
        ip = str(data.get("IP"))
        selectHost = "SELECT id FROM host WHERE ip = '" + ip + "'"
        self.cursor.execute(selectHost)
        resultHost = self.cursor.fetchone()

        if not resultHost :
            print("Nouvel hôte")
            insertHost = "INSERT INTO host (ip) VALUES ('" + ip + "')"
            self.cursor.execute(insertHost)
            self.cursor.execute(selectHost)
            resultHost = self.cursor.fetchone()
        else :
            print("Hôte existant")

        idIP = str(resultHost.get("id"))
        cpu = str(data.get("CPU"))
        insertCPU = "INSERT INTO mesure (host_id, valeur, date, type) VALUES ('" + idIP + "', '" + cpu + "', NOW(), 'CPU')"
        self.cursor.execute(insertCPU)
        print("CPU inséré")

        disk = str(data.get("DISK"))
        insertDISK = "INSERT INTO mesure (host_id, valeur, date, type) VALUES ('" + idIP + "', '" + disk + "', NOW(), 'DISK')"
        self.cursor.execute(insertDISK)
        print("DISK inséré")

        net = str(data.get("NET"))
        insertNET = "INSERT INTO mesure (host_id, valeur, date, type) VALUES ('" + idIP + "', '" + net + "', NOW(), 'NET')"
        self.cursor.execute(insertNET)
        print("NET inséré")

        ramt = str(data.get("RAMT"))
        insertRAMT = "INSERT INTO mesure (host_id, valeur, date, type) VALUES ('" + idIP + "', '" + ramt + "', NOW(), 'RAMT')"
        self.cursor.execute(insertRAMT)
        print("RAMT inséré")

        ramu = str(data.get("RAMU"))
        insertRAMU = "INSERT INTO mesure (host_id, valeur, date, type) VALUES ('" + idIP + "', '" + ramu + "', NOW(), 'RAMU')"
        self.cursor.execute(insertRAMU)
        print("RAMU inséré")

db = Database()

@app.route('/collect2', methods=["POST"])
def collect2():
    content = request.json
    print(str(content))
    data = json.loads(content)

    liste = ['IP', 'CPU', 'DISK', 'NET', 'RAMT', 'RAMU']
    verif = True
    listeData = []

    for i in data.keys():
        listeData.append(i)
    if len(liste) == len(listeData):
        k = 0
        while (k < len(liste)):
            if (liste[k] != listeData[k]):
                verif = False
            k += 1
    else:
        verif = False
    if not (isinstance(data.get('IP'), str) and isinstance(data.get('CPU'), (float, int)) and isinstance(data.get('DISK'), (float, int)) and isinstance(data.get('NET'), (float, int)) and isinstance(data.get('RAMT'), (float, int)) and isinstance(data.get('RAMU'), (float, int))):
        verif = False
    if (verif):
        print("Vérification valeur réussi")
        db.update(data)
    else:
        print("Erreur vérification valeur")

    return ("Return : "+str(content))

if __name__ == '__main__':
    app.run(debug=False, host = "0.0.0.0")
