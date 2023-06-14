#!/bin/bash
docker-compose build db backend
docker-compose up -d db backend

docker-compose exec backend chmod +x /openimis-be/openIMIS/custom_scripts/check_service_availability.sh
docker-compose exec backend bash /openimis-be/openIMIS/custom_scripts/check_service_availability.sh
docker-compose exec backend python /openimis-be/openIMIS/custom_scripts/import_data.py

