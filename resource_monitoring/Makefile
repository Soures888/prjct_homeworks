# Makefile
.PHONY: test

# concurrency levels
CONCURRENCY = 1 5 20
# endpoints
ENDPOINTS = mongoread esread

# run siege test with different concurrency levels and endpoints
test:
	@for endpoint in $(ENDPOINTS); do \
		for n in $(CONCURRENCY); do \
			echo "Running test on endpoint $$endpoint with concurrency $$n"; \
			./load_test.sh $$n $$endpoint; \
		done \
	done

