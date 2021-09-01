#!/bin/bash

#get ip
cp ../config.json .
S=$(jq -r '.server' config.json)

#kill any running container and remove
sudo docker kill se-api-container
sudo docker rm se-api-container

#remove image
ID=$(sudo docker images se-api-image -a -q)
sudo docker rmi $ID


#create image
sudo docker build -t se-api-image .
sudo docker save -o se-api-image.tar se-api-image
sudo chown david se-api-image.tar

# remove files
sudo rm config.json

#upload image to server
scp -r se-api-image.tar $S:~/Dev/stake-everything-api/

#kill and remove container sequence
echo "removing containers..."
ssh david@$S "sudo docker kill se-api-container"
ssh david@$S "sudo docker rm se-api-container"
ssh david@$S "sudo docker container ls -la"

#remove image
echo "removing image..."
ID=$(ssh david@$S "sudo docker images se-api-image -a -q")
ssh david@$S "sudo docker rmi $ID -f"

#load image
echo "loading image..."
ssh david@$S "sudo docker load -i Dev/stake-everything-api/se-api-image.tar"
ssh david@$S "sudo docker image ls"

echo "starting container..."
#start docker image sequence
ssh david@$S "sudo docker container run -d -p 80:5000 --name se-api-container se-api-image"

echo "upload sequence complete. container started."

