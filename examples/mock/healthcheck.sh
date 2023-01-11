curl localhost:3001/healthcheck

RETURN=$?

if [ $RETURN == 7 ];
then
  echo "Healthcheck failed, mockoon API not available (curl returned status code 7)"
  exit 1
fi
exit 0