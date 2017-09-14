import MySQLdb
import os
import paramiko
import socket

cnx = MySQLdb.connect(host="localhost", user="root", passwd="raspberry", db="home")
cursor = cnx.cursor()
query = 'SELECT sensor_ip FROM sensors'
cursor.execute(query)
r = cursor.fetchall()
for sensor_ip in r:
  host = str(sensor_ip)[2:-3]
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
  try:
    ssh.connect(host, username='pi',
      password='raspberry')
    stdin, stdout, stderr = ssh.exec_command(
      "ps axg | grep sensor.py")
    for line in stdout:
      if "pi/sensor.py" in line:
         print '\033[92m' + host + " is online and sensor process is running"
      else:
        print '\033[93m' + host " is online but no sensor process running"
  except:
    print '\033[91m' + "Could not connect to " + host
