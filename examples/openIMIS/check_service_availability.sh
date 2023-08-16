#!/bin/bash
set -euxo pipefail

apt-get install -y netcat

check_service() {
  local service=$1
  local port=$2
  local max_retries=10
  local try=0

  while [ $try -lt $max_retries ]; do
    nc -z $service $port
    result=$?

    if [ $result -eq 0 ]; then
      echo "$service is up!"
      return 0
    else
      echo "Waiting for $service ($try)... "
      sleep 30
    fi

    try=$((try + 1))
  done

  echo "$service failed to start in time."
  return 1
}

check_service backend 8000