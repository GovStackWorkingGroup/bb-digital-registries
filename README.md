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

## Run Cucumber tests

Cucumber-js is used to execute test harness to check compability of application
api with BB test definitions.

### Mock server

Launch the mock server from examples/mock folder. The instruction is located in
'examples/mock' folder in file README.md

### Cucumber tests

To install project's dependencies, navigate to folder 'test' and execute the
following command:

```
yarn install
```

Then to execute all tests scenarios use the following command:

```
yarn test
```

or

```
npx cucumber-js
```

To execute specific test scenario use the following command:

```
npx cucumber-js features/<file_name>
```

example:

```
npx cucumber-js features/data_update_or_create.feature
```
