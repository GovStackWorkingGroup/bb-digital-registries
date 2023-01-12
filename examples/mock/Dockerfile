FROM node:14-alpine

RUN npm install -g @mockoon/cli@2.2.1
COPY mockoon-digitalregistries.json ./mockoon-digitalregistries.json

# Do not run as root.
RUN adduser --shell /bin/sh --disabled-password --gecos "" mockoon
RUN chown -R mockoon ./mockoon-digitalregistries.json
USER mockoon

EXPOSE 3001

ENTRYPOINT ["/entrypoint.sh"]