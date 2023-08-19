package main

import (
	"log"
	"os"
	"sync"
	"time"
)

const (
	MESSAGES_COUNT_BY_THREAD = 1000
	PRODUCER_NUMBERS         = 6
	CONSUMER_NUMBERS         = 6
	QUEUE_NAME               = "benchmark_queue"
	REDIS_AOF_ADDRESS        = "localhost:6377"
	REDIS_RDB_ADDRESS        = "localhost:6378"
	BEANSTALKD_ADDRESS       = "localhost:11300"
)

func produce(queue Queue, wg *sync.WaitGroup) {
	// Return mess
	defer wg.Done()
	for i := 0; i < MESSAGES_COUNT_BY_THREAD; i++ {
		err := queue.push("very_important_message")
		if err != nil {
			log.Fatal(err)
		}
	}

}

func consume(queue Queue, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < MESSAGES_COUNT_BY_THREAD; i++ {
		msg, err := queue.pop()
		_ = msg
		if err != nil {
			log.Fatal(err)
		}
	}
}

type Stats struct {
	TotalTimeMs   int64
	ProduceTimeMs int64
	ConsumeTimeMs int64
}

func main() {
	args := os.Args[1:]

	// Get queue type
	var queueClient Queue
	var queueType string

	switch queueType = args[0]; queueType {
	case "redis-aof":
		queueClient = NewRedisQueue(REDIS_AOF_ADDRESS, QUEUE_NAME)
	case "redis-rdb":
		queueClient = NewRedisQueue(REDIS_RDB_ADDRESS, QUEUE_NAME)
	case "beanstalkd":
		var err error
		queueClient, err = NewBeanstalkdQueue(BEANSTALKD_ADDRESS, QUEUE_NAME)
		if err != nil {
			log.Panic(err)
		}
	default:
		log.Fatalf("Unknown queue type: %s", queueType)
	}

	defer queueClient.close()

	stats := Stats{}
	log.Printf("Run %d producers/consumers of type %s", PRODUCER_NUMBERS, queueType)
	wg := sync.WaitGroup{}

	// Run Producers
	produce_start := time.Now()
	for i := 0; i < PRODUCER_NUMBERS; i++ {
		wg.Add(1)
		go produce(queueClient, &wg)
	}
	wg.Wait()
	stats.ProduceTimeMs = time.Since(produce_start).Milliseconds()

	// Run Consumers
	consume_start := time.Now()
	wg = sync.WaitGroup{}
	for i := 0; i < CONSUMER_NUMBERS; i++ {
		wg.Add(1)
		go consume(queueClient, &wg)
	}
	wg.Wait()
	stats.ConsumeTimeMs = time.Since(consume_start).Milliseconds()
	stats.TotalTimeMs = stats.ConsumeTimeMs + stats.ProduceTimeMs

	log.Printf("Total time: %d ms", stats.TotalTimeMs)
	log.Printf("Produce time: %d ms", stats.ProduceTimeMs)
	log.Printf("Consume time: %d ms", stats.ConsumeTimeMs)
}
