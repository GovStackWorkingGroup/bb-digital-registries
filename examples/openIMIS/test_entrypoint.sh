#!/bin/bash
docker-compose build db backend
docker-compose up -d db backend

# exec inserted script in the container
#docker-compose exec backend python /openimis-be/openIMIS/custom_scripts/import_data.py

docker-compose exec backend chmod +x /check_service_availability.sh
docker-compose exec backend bash /check_service_availability.sh
docker-compose exec backend python /import_data.py
