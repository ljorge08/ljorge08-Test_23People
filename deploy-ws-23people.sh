#/bin/bash

#Stoping the app if is running

kill -9 $(ps -ef | grep WS_23people.py | grep python | awk '{print $2}')

#creating a backup of the last version in the server

days=`date +"%Y%m%d_%H%M"`
echo "Creating the backup"
zip /home/ljorge08/backup/bacukp_ws_23people_${days}.zip /home/ljorge08/ws/23people/

#Cleaning the folder repository

echo "Cleaning the local repository"
rm -rf /home/ljorge08/ws/23people/
mkdir /home/ljorge08/ws/23people/ 


echo "Cloning the project"
repository="https://github.com/ljorge08/ljorge08-Test_23People"
localFolder="/home/ljorge08/ws/23people/"

git clone $repository $localFolder

#Updating BD conf
echo "Updating BD conf"
cp /home/ljorge08/mysql.conf /home/ljorge08/ws/23people/conf

#Starting the application

echo "#Starting the application"
python /home/ljorge08/ws/23people/WS_23people.py &
