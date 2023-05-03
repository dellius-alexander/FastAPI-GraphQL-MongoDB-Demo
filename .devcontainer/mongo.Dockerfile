FROM mongo:5.0.16
EXPOSE 27017
COPY .devcontainer/config/mongo/mongo-init.js* /docker-entrypoint-initdb.d/mongo-init.js
COPY .devcontainer/config/mongo/mongod.conf* /etc/mongod.conf

