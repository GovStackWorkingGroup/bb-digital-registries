FROM node:14-alpine

RUN npm install -g @mockoon/cli@2.2.1

COPY /examples/mockoon/ /mockoon
COPY /api /mockoon/api
WORKDIR /mockoon
RUN npm install --loglevel=error
# Do not run as root.
RUN adduser --shell /bin/sh --disabled-password --gecos "" mockoon
# RUN chown -R mockoon ./mockoon-digitalregistries.json
RUN node api_organizer.js
WORKDIR /mockoon/api
USER mockoon

EXPOSE 3000

ENTRYPOINT ["mockoon-cli", "start", "--hostname", "0.0.0.0", "--daemon-off", "--data", "AssemblyApiDefinition.yaml"]

# Usage: docker run -p <host_port>:<container_port> mockoon-test