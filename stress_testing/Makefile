# Makefile
.PHONY: test

# concurrency levels
CONCURRENCY = 10 25 50 100

# run siege test with different concurrency levels and endpoints
test:
	for n in $(CONCURRENCY); do \
		echo "Running test with concurrency $$n"; \
		./load_test.sh $$n; \
	done

