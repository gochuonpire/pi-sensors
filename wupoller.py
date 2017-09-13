import requests
import _mysql as MySQLdb
import time

while True:
  print 'Polling Weather Underground'
  data = requests.get('http://api.wunderground.com/api/b5745e9cacaf559d/conditions/q/VA/Great_Falls.json').json()

  cnx = MySQLdb.connection(host="localhost", user="root", passwd="raspberry", db="home")

  cursor = cnx.cursor()
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  update_insert = ("INSERT INTO weather "
                  "(time, observation_time, temp, humidity, pressure, wind_degrees, wind_mph, wind_gust_mph, solarradiation, precip_1hr_in) "
                  " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

  observation_time = data['current_observation']['observation_time_rfc822']
  temp_f = data['current_observation']['temp_f']
  humidity = data['current_observation']['relative_humidity']
  pressure = data ['current_observation']['pressure_mb']
  wind_degrees = data ['current_observation']['wind_degrees']
  wind_mph = data ['current_observation']['wind_mph']
  wind_gust_mph = data ['current_observation']['wind_gust_mph']
  solarradiation = data ['current_observation']['solarradiation']
  precip_1hr_in = data ['current_observation']['precip_1hr_in']

  update_data = (time, date, temp_f, humidity, pressure, wind_degrees, wind_mph, wind_gust_mph, solarradiation, precip_1hr_in)
  cursor.execute(update_insert, update_data)
  cnx.commit()
  cnx.close()

  print 'Done'
  time.sleep(300.0 - ((time.time() - starttime) % 60.0))