#!/bin/bash
docker-compose build db backend
docker-compose up -d db backend

docker-compose exec backend chmod +x /check_service_availability.sh
docker-compose exec backend bash /check_service_availability.sh
docker-compose exec backend python /import_data.py
