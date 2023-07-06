#!/bin/bash
docker-compose build --no-cache db backend

docker-compose up -d db backend

docker-compose exec backend chmod +x /check_service_availability.sh
docker-compose exec backend bash /check_service_availability.sh
docker-compose exec backend ls
echo "python createTestCustomParameters.py"
docker-compose exec backend python /createTestCustomParameters.py

container_id=$(docker-compose ps -q backend)
echo "ls"
docker-compose exec backend ls
echo "pwd"
docker-compose exec backend pwd
docker-compose exec backend ls /openimis-be/openIMIS

docker cp $container_id:/openimis-be/openIMIS/testCustomParameters.json ./testCustomParameters.json

docker-compose exec backend python /import_data.py
