#! /bin/bash

index="journal-articles"
mapping_path=$(pwd)"/scripts/es/mappings"

echo "Creating elasticsearch index: $index"

curl -XDELETE "http://localhost:9200/$index"
echo ""
curl -XPUT "http://localhost:9200/$index" -H 'Content-Type: application/json'
echo ""
curl -XPUT "http://localhost:9200/$index/_mapping" -H 'Content-Type: application/json' --data @$mapping_path/journal.json
echo ""
