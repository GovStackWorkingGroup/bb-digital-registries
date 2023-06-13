#!/bin/bash

docker-compose up --build -d db backend

# exec inserted script in the container
docker-compose exec backend python /openimis-be/openIMIS/custom_scripts/import_data.py

