#!/bin/bash

date_tag=$(date +%Y-%m-%d)

docker build --no-cache -t mcp-gitignore:$date_tag .
docker tag mcp-gitignore:$date_tag mcp-gitignore:latest
