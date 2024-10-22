#!/bin/bash

echo "Validating cluster creation..."
if kubectl get nodes; then
    echo "Cluster creation validated successfully!"
else
    echo "Cluster creation failed!" >&2
    exit 1
fi 