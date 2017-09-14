#!/bin/bash
python /home/pi/Desktop/pi-sensors/wupoller.py &
python /home/pi/Desktop/pi-sensors/nest_poll.py &
python /home/pi/Desktop/pi-sensors/reader.py &
python /home/pi/Desktop/pi-sensors/contingency.py &
