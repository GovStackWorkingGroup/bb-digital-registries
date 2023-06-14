#!/bin/bash
docker-compose build db backend
docker-compose up -d db backend

# exec inserted script in the container
docker-compose exec backend python /openimis-be/openIMIS/custom_scripts/import_data.py

