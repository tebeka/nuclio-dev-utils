#!/bin/bash
# Run the dashboard

set -e

go build ./cmd/dashboard
docker run \
    -p 8070:8070 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /tmp:/tmp \
    nuclio/dashboard:latest-amd64
