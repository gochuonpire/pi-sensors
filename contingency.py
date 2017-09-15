import urllib
import time
import MySQLdb
import datetime
import smtplib
import gemail
import threading

# Checks to make sure sensors/controller are receiving data. Reports problems
def f():
  threading.Timer(900, f).start()
  print 'Checking Sensors'
  checkSensors()
  print 'Checking Controller(this)'
  checkController()
  print 'Done'

def checkSensors():
  cnx = MySQLdb.connect(host="localhost", user="root", passwd="raspberry", db="home")
  cursor = cnx.cursor()
  query = "SELECT sensor_id FROM sensors"
  cursor.execute(query)
  r=cursor.fetchall()
  for s_id in r:
    recent = "SELECT `time` FROM observations WHERE sensor = %s ORDER BY `time` DESC LIMIT 1" % (s_id)
    cursor.execute(recent)
    rec=cursor.fetchall()
    for ltime in rec:
      ts = time.time()
      timestamp = datetime.datetime.fromtimestamp(ts)
      sensorstamp = ltime[0]
      delta = (timestamp-sensorstamp).total_seconds()
      if delta > 120:
        message =  'Something is wrong with the raspberry pi sensor ' + str(s_id[0]) + ', data has not been collected for ' + str(delta) + 'seonds'
        gemail.email(message)
  cnx.close()

def checkController():
  cnx = MySQLdb.connect(host="localhost", user="root", passwd="raspberry", db="home")
  cursor = cnx.cursor()
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts)
  query = "SELECT `id`,`time` FROM observations ORDER BY `time` DESC LIMIT 1"
  cursor.execute(query)
  r=cursor.fetchall()
  newstamp=0
  for s_id, s_time in r:
    newstamp = s_time
  serverstamp = datetime.datetime.strptime(newstamp,'%Y-%m-%d %H:%M:%S')
  delta = (timestamp-serverstamp).total_seconds()
  if delta > 65:
    message = "Alert, controller down for %s seconds" % str(delta)
    gemail.email(message)
  query = "SELECT `id`, `time` FROM weather ORDER BY `time` DESC LIMIT 1"
  cursor.execute(query)
  r=cursor.fetchall()
  for w_id, w_time in r:
    wstamp = w_time
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts)
  serverstamp = datetime.datetime.strptime(wstamp, '%Y-%m-%d %H:%M:%S')
  wdelta = (timestamp-serverstamp).total_seconds()
  if wdelta > 350:
    message = "Alert, weather polling down for %s seconds" % str(delta)
    gemail.email(message)
  query = "SELECT `id`, `time` FROM nest_polls ORDER BY `time` DESC LIMIT 1"
  cursor.execute(query)
  r=cursor.fetchall()
  for n_id, n_time in r:
    nstamp = n_time
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts)
  serverstamp = datetime.datetime.strptime(nstamp, '%Y-%m-%d %H:%M:%S')
  ndelta = (timestamp-serverstamp).total_seconds()
  if ndelta > 350:
    message = "Alert, nest polling down for %s seconds" % str(delta)
    gemail.email(message)
  cnx.close()

f()
