#!/bin/sh

# Wait for Elasticsearch to be ready
until curl -sS "http://localhost:9200/_cat/health?h=status" | grep -q "green\|yellow"; do
  sleep 1
done

# Initialize the "log_mapping" index with mappings
curl -X PUT "http://localhost:9200/logingestor_data" -H "Content-Type: application/json" -d @/usr/share/elasticsearch/log_mapping.json

# Start Elasticsearch
exec /usr/local/bin/docker-entrypoint.sh