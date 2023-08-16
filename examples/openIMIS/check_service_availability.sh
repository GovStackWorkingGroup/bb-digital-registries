#!/bin/bash

healthcheckApiCall() {
    echo "Sending test request, result:"
    echo "-----"
    curl localhost:3333 > /dev/null
    RETURN=$?
    if [ $RETURN -ne 0 ];
    then
      echo "Api healthcheck call failed"
      docker-compose logs backend
      return 1
    fi
    echo "-----"
    echo "Success in calling healtcheck API endpoint"
    return 0
}

waitForAPI() {
    echo "Testing API availability..."
    retries=10
    interval=20
    notAvailable=1
    while [ $retries -ge 0 ] && [ $notAvailable -ne 0 ]
    do
      healthcheckApiCall
      notAvailable=$?
      retries=$(( $retries - 1 ))
      if [ $retries -ne 5 ]
      then 
         sleep 1
      fi
    done

    if [ $notAvailable -eq 1 ]
    then
      echo "Gherkin tests will not be executed as API is not available."
      exit 1
    fi
    echo "API Available."
    return 0
}

waitForAPI