#! /bin/bash

docker build -t remix docker_remix &
docker build -t raiden docker_raiden &
docker build -t lamden-api docker_lamden_api &
docker build -t explorer-server docker_explorer  &
