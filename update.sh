while read SERVER PASSWORD
do
  sshpass -p "$PASSWORD" scp sensor.py pi@"$SERVER":/home/pi/
done <./server.txt
