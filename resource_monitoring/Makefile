# Makefile
.PHONY: test

# concurrency levels
CONCURRENCY = 5 20 50
# endpoints
ENDPOINTS = mysqlread esread

# run siege test with different concurrency levels and endpoints
test:
	@for endpoint in $(ENDPOINTS); do \
		for n in $(CONCURRENCY); do \
			echo "Running test on endpoint $$endpoint with concurrency $$n"; \
			./load_test.sh $$n $$endpoint; \
		done \
	done

