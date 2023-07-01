#!/bin/bash
# Pass concurrency level and endpoint as command-line arguments
concurrency=$1
endpoint=$2
# URL to be tested
url=http://localhost/fastapi/$endpoint
# Run Siege
siege -c $concurrency -t 90S -b $url >> test.txt
echo "Sleeping for 90 seconds"
sleep 90