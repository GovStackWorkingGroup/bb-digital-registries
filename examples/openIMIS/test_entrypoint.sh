#!/bin/bash
set -e

docker-compose build --no-cache db backend
docker-compose run backend manage migrate

docker-compose up -d db backend


timeout=$((SECONDS + 120))
until docker-compose exec backend echo "Service is up" || [ $SECONDS -gt $timeout ]; do
    sleep 1
done

if [ $SECONDS -gt $timeout ]; then
    echo "Timed out waiting for the backend service to start."
    exit 1
fi

docker-compose exec backend chmod +x /check_service_availability.sh
sleep 120
# docker-compose exec backend bash /check_service_availability.sh

docker-compose logs backend
docker-compose exec backend python /createTestCustomParameters.py
container_id=$(docker-compose ps -q backend)
docker cp $container_id:/openimis-be/openIMIS/testCustomParameters.json ./testCustomParameters.json

docker-compose exec backend python /import_data.py
