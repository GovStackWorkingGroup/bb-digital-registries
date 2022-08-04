# GovStack Building Block Template

This template is intended to be used by the various GovStack building block
repos. Each building block repo will have at least 4 main sections, outlined in
the directory structure below.

## Gitbook and the published "Building Block Specifications" document

Note that pushes to the `main` branch will automatically trigger a Gitbook build
and deployment from the `/spec` directory.

## Repo Structure

```sh
README.md
/spec # the markdown files which are used to build the specification in GitBook
/api # the openapi specification
/test # the test plan and tests
  plan.md
/examples # examples for deploying, configuring, and testing applications which implement the behaviors specified by this building block
  /application-a
    README.md # instructions for deployment/testing
    docker-compose.yaml # example deployment file
      db
      web
      adaptor
      security-server
    Caddyfile # example config for "adaptor"
    Dockerfile # dockerfile to build "adaptor"
  /application-b
  /application-c
```
