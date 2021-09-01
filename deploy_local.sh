#!/bin/bash

#get ip
cp ../config.json .
S=$(jq -r '.server' config.json)

#kill running container and remove it
sudo docker kill se-api-container
sudo docker rm se-api-container

#remove image
ID=$(sudo docker images se-api-image -a -q)
sudo docker rmi $ID

#create image
sudo docker build -t se-api-image .

#run image
sudo docker container run -d -p 80:5000 --name se-api-container se-api-image

# remove files
sudo rm config.json
