# Redis Master-Slaves cluster with sentinel for monitoring and failover

## Description

This project is a simple example of how to create a Redis cluster with master-slaves and sentinel for monitoring and failover.

## Requirements

- Docker
- Docker Compose

## Python script probabilistic cache eviction

With this approach, each process may recompute the cache value before its expiration by making an independent probabilistic decision, where the probability of performing the early recomputation increases as we get closer to the expiration of the value. Since the probabilistic decision is made independently by each process, the effect of the stampede is mitigated as fewer processes will expire at the same time.

## Simple realisation example

`./python_script/script.py`