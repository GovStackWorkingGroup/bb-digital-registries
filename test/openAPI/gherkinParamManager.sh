#!/bin/bash

# Define paths to custom and default parameters files
CUSTOM_JSON_PATH="testCustomParameters.json"
DEFAULT_JSON_PATH="testDefaultParameters.json"

if [ -f $CUSTOM_JSON_PATH ] && [ -f $DEFAULT_JSON_PATH ]; then
   # Both files exist, compare their keys
  CUSTOM_KEYS=$(jq -r 'keys[]' $CUSTOM_JSON_PATH | sort)
  DEFAULT_KEYS=$(jq -r 'keys[]' $DEFAULT_JSON_PATH | sort)

  if [ "$CUSTOM_KEYS" != "$DEFAULT_KEYS" ]; then
    echo "Keys in $CUSTOM_JSON_PATH and $DEFAULT_JSON_PATH do not match. Exiting."
    exit 1
  fi

  PARAMETERS_PATH="../$CUSTOM_JSON_PATH"
elif [ -f $DEFAULT_JSON_PATH ]; then 
  # Only default parameters file exists, use it for substitution
  PARAMETERS_PATH="../$DEFAULT_JSON_PATH"
else
  echo "No parameters file found. Continuing without parameter substitution."
  PARAMETERS_PATH=""
fi

if [ ! -z $PARAMETERS_PATH ]; then
  echo "Replacing placeholders in .feature files using $PARAMETERS_PATH."
  cd features
  for feature_file in *.feature
  do
    while IFS="=" read -r key value
    do
      sed -i "s/\${$key}/$value/g" "$feature_file"
    done < <(jq -r 'to_entries|map("\(.key)=\(.value|tostring)")|.[]' $PARAMETERS_PATH)
  done
fi
