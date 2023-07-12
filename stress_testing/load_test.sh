#!/bin/bash
# Pass concurrency level and endpoint as command-line arguments
concurrency=$1
# Run Siege
siege -c $concurrency -t 60S -f stress_testing_urls.txt >> test.txt
echo "Sleeping for 30 seconds"
sleep 30