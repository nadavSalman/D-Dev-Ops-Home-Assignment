#!/bin/bash

echo "test"


# # dump
# mongodump --uri "$ATLAS_URI" --archive > db.dump

# # load
# PRIMARY_HOST=$(mongosh "mongodb://my-user:$MONGODB_LOCAL_PASSWORD@devops-mongodb-svc.mongodb.svc.cluster.local:40333" --quiet --eval "rs.status()" --json | jq -r '.members[] | select(.stateStr == "PRIMARY") | .name' | cut -d':' -f1)
# echo "Primary Host : $PRIMARY_HOST"

# # restore
# mongorestore --uri "mongodb://my-user:$MONGODB_LOCAL_PASSWORD@$PRIMARY_HOST:40333" --archive < db.dump