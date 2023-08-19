package main

import (
	"context"
	"log"
	"time"

	"github.com/beanstalkd/go-beanstalk"
	"github.com/redis/go-redis/v9"
)
type Queue interface {
	pop() (string, error)
	push(data string) (error)
	close()
}

type BeanstalkdQueue struct {
	conn      *beanstalk.Conn
	tubeSet   *beanstalk.TubeSet
	tubeName  string
}

type RedisQueue struct {
	client *redis.Client
	queueName string
}


func NewRedisQueue(address string, queueName string) *RedisQueue {
	rdb := redis.NewClient(&redis.Options{
		Addr: address, // "localhost:6379"
		DB:   0,       // use default DB
	})

	return &RedisQueue{
		client:    rdb,
		queueName: queueName,
	}
}

func NewBeanstalkdQueue(address, tubeName string) (*BeanstalkdQueue, error) {
	conn, err := beanstalk.Dial("tcp", address) // "localhost:11300"
	if err != nil {
		return nil, err
	}

	ts := beanstalk.NewTubeSet(conn, tubeName)
	return &BeanstalkdQueue{
		conn:     conn,
		tubeSet:  ts,
		tubeName: tubeName,
	}, nil
}

// Realisation of  Redis
func (queue *RedisQueue) pop() (string, error) {
	ctx := context.Background()
	result, err := queue.client.BLPop(ctx, 1*time.Second, queue.queueName).Result()

	if err != nil {
		return "", err
	}
	return result[1], nil // result[0] is the queueName, result[1] is the value
}

func (queue *RedisQueue) push(data string) (error) {
	ctx := context.Background()
	err := queue.client.RPush(ctx, queue.queueName, data).Err()
	return err
}

func (queue *RedisQueue) close() {
	queue.client.Close()
}

// Realisation of Beanstalkd
func (queue *BeanstalkdQueue) pop() (string, error) {
	id, body, err := queue.conn.Reserve(1 * time.Second)
	if err != nil {
		log.Println("Error: ", err)
		return "", err
	}
	queue.conn.Delete(id)
	return string(body), nil
}

func (queue *BeanstalkdQueue) push(data string) (error) {
	_, err := queue.conn.Put([]byte(data), 1, 0, 120) // using default priority, delay, and TTR
	return err
}

func (queue *BeanstalkdQueue) close() {
	queue.conn.Close()
}