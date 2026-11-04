# openIMIS historical example

This directory preserves an openIMIS integration developed for the earlier generated CRUD interface. It is not evidence of conformance with the current Digital Registries specification.

The container images and integration dependencies are historical and may no longer be available. Review them before attempting to reproduce the environment.

## Local configuration

From the repository root, copy the public template to the ignored local configuration file:

```sh
cp examples/openIMIS/.env.example examples/openIMIS/.env
```

Set local values for `DB_PASSWORD` and `OPENIMIS_ADMIN_PASSWORD`. Keep `.env` untracked. `OPENIMIS_ADMIN_USERNAME` is configurable and defaults to the historical administrator name in the example template.

Validate interpolation before starting any containers:

```sh
docker compose --env-file examples/openIMIS/.env \
  -f examples/openIMIS/docker-compose.yml config
```

Compose stops with an explicit message when either required password or the administrator username is missing or empty.
