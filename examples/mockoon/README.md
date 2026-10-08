# Mockoon legacy API

> This mock targets the previous generated CRUD OpenAPI files. It is not a 3.0.0-alpha.2 Registry mock or conformance target.

This is a mock application for the legacy Digital Registries OpenAPI surface.


## Setup
To run dockerized version of mocked API use shell script 
`test_entrypoint.sh` (requires `docker` and `docker-compose`). 
By default, API is available on port `3333`, application runs on port `3001` in Docker host. Dockerfile was created using mockoon-cli.

## Changes in API definition
To introduce changes in API definition it is necessary to change content of `mockoon-digitalregistries.json` file. It can be done using [mockoon application](https://mockoon.com/). After following instalation, API Spec can be opened from application navigation bar `File > Open environment > Select mockoon-digitalregistries.json`. Dockerized instance of application is not hot-reloaded, therefore it's necessary to restart server for changes to be applied.  
