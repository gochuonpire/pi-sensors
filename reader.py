import time
import MySQLdb
import socket
from datetime import datetime as dt, timedelta
import os
import threading

def f():
 threading.Timer(60, f).start()
 print 'Polling Data'
 pollPis()
 now = dt.now()
 if now-timedelta(hours=24) <= starttime <= now+timedelta(hours=24):
  print 'Rebooting later'
 else:
  print 'Rebooting now...'
  os.system('reboot')
 print 'Done'

def pollPis():

  cnx = MySQLdb.connect(host="localhost", user="root", passwd="raspberry", db="home")
  cursor = cnx.cursor()
  ts = time.time()
  timestamp = dt.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

  query = "SELECT sensor_id, sensor_ip, sensor_port from sensors"

  cursor.execute(query)

  returnedRows = cursor.fetchall()

  for (sensor_id, sensor_ip, sensor_port) in returnedRows:
   TCP_IP = sensor_ip
   TCP_PORT = sensor_port
   BUFFER_SIZE = 1024
   MESSAGE = "send"
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(1)
   try:
    s.connect_ex((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
   except:
    message = "Error connecting to " + sensor_ip + ":" + str(sensor_port)
    print message
    continue
   else:
    print 'Successfully connected to ' + sensor_ip + ":" + str(sensor_port)
   newdata = data.split()
   update_insert = ("INSERT INTO observations "
    "(sensor, time, temp, humidity, pressure) "
    "VALUES (%s, %s, %s, %s, %s)")
   update_data = (sensor_id, timestamp, float(newdata[0]), float(newdata[1]), float(newdata[2]))
   cursor.execute(update_insert, update_data)

  cnx.commit()
  cnx.close()
  return True

starttime=datetime.now()

f()
