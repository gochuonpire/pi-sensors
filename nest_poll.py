import nest
import MySQLdb
import time
import datetime
import threading
# Polls Nest devices and stores some data
# None of this is really ready to use for other Nest setups yet
def f():
  threading.Timer(300, f).start()
  print 'Polling Nest Thermostats'
  pollNests()
  print 'Done'

def pollNests():
  client_id = 'e49c6ec1-db2e-49a3-bff6-1ac9ce422def'
  client_secret = 'YEX7AG1hiuz6WJCYNs3eO5xFY'
  access_token_cache_file = 'nest.json'
  napi = nest.Nest(client_id=client_id, client_secret=client_secret, access_token_cache_file=access_token_cache_file)
  cnx = MySQLdb.connect(host="localhost", user="root", passwd="raspberry", db="home")
  cursor = cnx.cursor()
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  if napi.authorization_required:
    print('Go to ' + 'https://home.nest.com/login/oauth2?client_id=e49c6ec1-db2e-49a3-bff6-1ac9ce422def&state=STATE' + ' to authorize, then enter PIN below')
    pin = raw_input("pin: ")
    napi.request_token(pin)
  for device in napi.thermostats:
    if device.name == 'Downstairs':
      nest_id = 2
    elif device.name == 'Upstairs':
      nest_id = 1
    update_query = ("INSERT INTO nest_polls "
      "(time, nest, fan, temp, humidity, target_low, target_high, eco_heat, eco_cool) "
      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    fan = device.fan
    temp = device.temperature
    humidity = device.humidity
    target_low = device.target[0]
    target_high = device.target[1]
    eco_heat = device.eco_temperature[0]
    eco_cool = device.eco_temperature[1]
    update_data = (timestamp, nest_id, fan, temp, humidity, target_low, target_high, eco_heat, eco_cool)
    cursor.execute(update_query, update_data)
  cnx.commit()
  cnx.close()

f()
