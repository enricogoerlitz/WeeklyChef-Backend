#!/bin/bash

# bash dhub.recipe.build.push.sh 
# Define variables
DOCKERFILE_PATH="./docker/dev/dockerfile.service.recipe"
IMAGE_NAME="weeklychef-recipe-service"
DOCKERHUB_USERNAME="enricogoerlitz"
VERSION="latest"

# Build the Docker image
docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH .

# Tag the Docker image
docker tag $IMAGE_NAME $DOCKERHUB_USERNAME/$IMAGE_NAME:$VERSION

# Log in to Docker Hub
docker login

# Push the Docker image to Docker Hub
docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:$VERSION
