# Updating your sensors/controller
### Updating controller
To download updates, just navigate to your pi-sensors folder and run:
```
git pull
```
To get the controller running the new files, just reboot.
### Updating sensors
After that, the only thing left is to copy sensor.py to all of your sensors. There is a script to help, but you need to set it up manually first. You could also setup a samba server and mount it on every sensor to update automatically.
For the script, you need to create a server.txt file (in the same directory as update.sh) containing the ip address of every sensor and the associated password. An example line would look like this:
```
192.168.1.57 raspberry
```
Next, just run update.sh on your controller and it will copy the sensor.py file to all of the sensors found in the text file. This is just a placeholder, I am going to be making a python updater to read all of your sensors in MySQL to avoid setting up more files.
