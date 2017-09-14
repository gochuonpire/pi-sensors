# Script Setup
### Setting up the server/controller
I decided to use a pi3 w/ raspbian jessie as the server, it could realistically be done with any pi or linux machine. If you do use a raspberry pi of some sort, you'll need to do some initial setup. Run each of these commands and go through the installs accordingly. Keep in mind, things may vary depending on what you're running.
```
sudo apt-get install mysql-server python-mysqldb
sudo pip3 install requests
sudo apt-get install python-mysqldb
```
Next you'll want to get all of the necessary files onto your controller, one easy way to do this is to just install git and clone the repo, to do that you'll need to install git first.
```
sudo apt-get install git-all
```
To install pi-sensors with git, run the following command in the directory you with to install to (w raspbian anywhere is fine, /home/pi works fine)
```
git clone https://github.com/gochuonpire/pi-sensors.git
```
Next we need to set the scripts to start automatically. Run the following command to edit rc.local:
```
sudo nano /etc/rc.local
```
Copy starter.sh to / (or dont, but this is the easiest way to do autostart on raspbian).
Before the exit 0 at the bottom of the file, add the following:
```
sh ./starter.sh
```

### Setting up the sensors
For the sensors, I used raspberry pi zero Ws with raspbian jessie lite. To install the necessary software, run these commands:
```
sudo wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo apt-get install build-essential libi2c-dev i2c-tools python-dev libffi-dev
sudo pip install smbus-cffi
sudo apt-get install python-mysqldb
sudo wget -O bme280.py http://bit.ly/bme280py
```
Next, you need to add autostarting just like last time, run this command:
```
sudo nano /etc/rc.local
```
Add the following before the exit 0:
```
python /home/pi/sensor.py
```
Next we need to turn on i2c, run the following command and then navigate to (5) Interfacing Options. Then p5 enable i2c.
```
sudo raspi-config
```
Reboot your pi0w and you are ready to go.

### Setting up the MySQL Database
We used the following schema:
```
CREATE TABLE `observations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sensor` tinyint(4) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `temp` smallint(6) NOT NULL,
  `humidity` tinyint(4) NOT NULL,
  `pressure` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sensor` (`sensor`),
  CONSTRAINT `observations_ibfk_1` FOREIGN KEY (`sensor`) REFERENCES `sensors` (`sensor_id`)
)

CREATE TABLE `sensors` (
  `sensor_id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `sensor_name` varchar(50) NOT NULL,
  `sensor_mac` char(12) NOT NULL,
  `sensor_ip` varchar(15) NOT NULL,
  `sensor_port` mediumint(9) DEFAULT NULL,
  `floor` enum('First','Second','Ground') DEFAULT NULL,
  PRIMARY KEY (`sensor_id`)
)

CREATE TABLE `nests` (
	`nest_id` tinyint(4) NOT NULL AUTO_INCREMENT,
	`nest_name` varchar(11) NOT NULL,
	PRIMARY KEY (`nest_id`)
)

CREATE TABLE `nest_polls` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`nest` tinyint(4) NOT NULL,
	`fan` BOOLEAN NOT NULL,
	`temp` smallint(6) NOT NULL,
	`humidity` tinyint(4) NOT NULL,
	`target_low` tinyint(4) NOT NULL,
	`target_high` tinyint(4) NOT NULL,
	`eco_heat` tinyint(4) NOT NULL,
	`eco_cool` tinyint (4) NOT NULL,
	PRIMARY KEY (`id`),
	KEY `nest` (`nest`),
	CONSTRAINT `nest_polls_ibfk_1` FOREIGN KEY (`nest`) REFERENCES `nests` (`nest_id`)
)
```
The sensors are then manually added to the table along with a chosen port. MAC addresses are unused and just for additional identification purposes.
