# -*- coding: utf-8 -*
from flask import Markup
from flask import Flask
from flask import render_template
from flask import json
import pymysql



app = Flask(__name__, static_url_path='/static')

connection = pymysql.connect(host='192.168.3.97', user='test', password='123', db='base', cursorclass=pymysql.cursors.DictCursor)

test = connection or 'merde'

print(test)

def pourcentage_ram(ramt, ramu):

    ram = []

    print("ramt")
    print(ramt)
    print("ramu")
    print(ramu)

    for total, ip in ramt:
        for utilise, ipu in ramu:
            if ip == ipu:
                ram.append(((utilise/total)*100, ip))

    print("ram")
    print(ram)

    return ram

def refresh():
    cpu = []
    disk = []
    net = []
    ramu = []
    ramt = []
    mesure_date = []
    ip = []

    with connection.cursor() as cursor:


        # Read a single record
        sql_cpu = "SELECT mon_host.ip, ma_mesure.valeur, ma_mesure.type, ma_mesure.date " \
                  "FROM mesure AS ma_mesure INNER JOIN host AS mon_host ON ma_mesure.host_id = mon_host.id " \
                  "WHERE type='CPU' limit 100"

        cursor.execute(sql_cpu)
        result_cpu = cursor.fetchone()

        while result_cpu:
            print(result_cpu)

            cpu.append(result_cpu['valeur'])
            mesure_date.append(result_cpu['date'])
            ip.append(result_cpu['ip'])

            result_cpu = cursor.fetchone()



            # Read a single record
        sql_disk = "SELECT mon_host.ip, ma_mesure.valeur, ma_mesure.type, ma_mesure.date " \
                   "FROM mesure AS ma_mesure INNER JOIN host AS mon_host ON ma_mesure.host_id = mon_host.id " \
                   "WHERE type='DISK' limit 100"

        cursor.execute(sql_disk)
        result_disk = cursor.fetchone()

        while result_disk:
            print(result_disk)

            disk.append(result_disk['valeur'])
            mesure_date.append(result_disk['date'])
            ip.append(result_disk['ip'])

            result_disk = cursor.fetchone()




        # Read a single record
        sql_net = "SELECT mon_host.ip, ma_mesure.valeur, ma_mesure.type, ma_mesure.date " \
                  "FROM mesure AS ma_mesure INNER JOIN host AS mon_host ON ma_mesure.host_id = mon_host.id " \
                  "WHERE type='NET' limit 100"

        cursor.execute(sql_net)
        result_net = cursor.fetchone()

        while result_net:
            print(result_net)

            net.append(result_net['valeur'])
            mesure_date.append(result_net['date'])
            ip.append(result_net['ip'])

            result_net = cursor.fetchone()




        # Read a single record
        sql_ram = "SELECT mon_host.ip, ma_mesure.valeur, ma_mesure.type, ma_mesure.date " \
                  "FROM mesure AS ma_mesure INNER JOIN host AS mon_host ON ma_mesure.host_id = mon_host.id " \
                  "WHERE type='RAMU' limit 100"

        cursor.execute(sql_ram)
        result_ram = cursor.fetchone()

        while result_ram:
            print(result_ram)

            ramu.append((result_ram['valeur'], result_ram['ip']))
            mesure_date.append(result_ram['date'])
            ip.append(result_ram['ip'])

            result_ram = cursor.fetchone()




        # Read a single record
        sql_ramt = "SELECT DISTINCT mon_host.ip, AVG(ma_mesure.valeur) AS valeur" \
                   " FROM mesure AS ma_mesure INNER JOIN host AS mon_host ON ma_mesure.host_id = mon_host.id" \
                   " WHERE type='RAMT' GROUP BY mon_host.ip "

        cursor.execute(sql_ramt)
        result_ramt = cursor.fetchone()

        while result_ramt:
            print(result_ramt)

            ramt.append((result_ramt['valeur'], result_ramt['ip']))
            ip.append(result_ramt['ip'])

            result_ramt = cursor.fetchone()


    print(ramt, ramu)

    ram = pourcentage_ram(ramt, ramu)

    return [cpu, disk, ram, net]


@app.route("/")
def chart():
    # Connect to the database

    data = refresh()

    return render_template('chart.html', set1=data[0], set2=data[1], set4=data[3], set3=data[2])


if __name__ == "__main__":
    app.run()