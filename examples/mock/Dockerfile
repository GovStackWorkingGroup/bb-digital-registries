FROM node:14-alpine


RUN apk --no-cache add curl

RUN npm install -g @mockoon/cli@2.2.1
RUN npm install -g express --loglevel=error
RUN npm install -g forever --loglevel=error

COPY mockoon-digitalregistries.json ./mockoon-digitalregistries.json
COPY entrypoint.sh ./entrypoint.sh
COPY healthcheck.sh ./healthcheck.sh

# Do not run as root.
RUN adduser --shell /bin/sh --disabled-password --gecos "" mockoon
RUN chown -R mockoon ./mockoon-digitalregistries.json
RUN chown -R mockoon ./entrypoint.sh
RUN chown -R mockoon ./healthcheck.sh

USER mockoon

EXPOSE 3001
EXPOSE 4422 

ENTRYPOINT ["/entrypoint.sh"]
# Usage: docker run -p <host_port>:<container_port> mockoon-test