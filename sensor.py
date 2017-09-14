#!/usr/bin/python
#!/usr/bin/env python

import MySQLdb
import socket
import time
import bme280
from datetime import datetime as dt, timedelta
import os
import urllib

# Opens TCP up until reader connects, opens again after 5 seconds
# Spaghetti will be dealt with at a later date
def pollSensor():
 temperature,pressure,humidity = bme280.readBME280All()
 strData = str(temperature) + " " + str(humidity) + " " + str(pressure)
 return strData

TCP_IP = "127.0.0.1"
TCP_PORT = 5000

starttime=dt.now()

cnx = MySQLdb.connect(host="192.168.1.56", user="root", passwd="raspberry", db="home")
cursor = cnx.cursor()

si = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
si.connect(("8.8.8.8", 80))
sip = si.getsockname()[0]
si.close()

TCP_IP =  sip

query = "SELECT sensor_port FROM sensors WHERE sensor_ip = \'" + sip + "\'"
print(query)
cursor.execute(query)

returnedRows = cursor.fetchall()

cnx.close()

for(sensor_port) in returnedRows:
 TCP_PORT = sensor_port[0]

print(TCP_PORT)
while True:
 print 'Waiting for Request'

 BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.bind((TCP_IP, TCP_PORT))
 s.listen(1)

 conn, addr = s.accept()
 print 'Connection address:', addr
 while 1:
   try:
     now = dt.now()
     if now-timedelta(hours=6) <= starttime <= now+timedelta(hours=6):
      print 'Rebooting later'
     else:
      print 'Rebooting now...'
      gemail.email(message)
      os.system('reboot')
     data = conn.recv(BUFFER_SIZE)
     if not data: break
     print "received data:", data
     newData = pollSensor()
     conn.send(newData)  # echo
    except:
     message = "Error connecting"
     print message
     continue
    else:
     print "Successfully connected"

 conn.close()
 time.sleep(5)
