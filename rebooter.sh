for host in $(< servers.txt );
do
        sshpass -p raspberry ssh -o StrictHostKeyChecking=no pi@$host 'sudo shutdown -r +1 && exit'
done
