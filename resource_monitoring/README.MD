# Resource Monitoring Task

# Встановлення

1. `docker-compose up -d --build` - Запуск контейнерів
2. Виповніть curl запит для генерації тестових даних для MongoDB та ES
```
curl -X 'GET' \
'http://localhost/fastapi/generate_data' \
-H 'accept: application/json'
```
3. Запустити тести на нагрузку `make run`. \
Спочатку будуть запущені тести на MongoDB в 5/20/50, потім на ES

# Тести

Docker конфигурація на моїй тестовій машині:

![Docker](https://i.imgur.com/vY2R4jT.jpg)

FatAPI конфігурація:

- 5 воркерів

Загальні результати тестів:

![Full Results](https://i.imgur.com/htTgSeL.jpg)

### [Більше скриншотів](https://imgur.com/a/fag1QjU)

Тобто, як ми бачимо з результатів, при повному навантаженні всіх воркерів нагрузка зростає до ~90 відсодків \
Але при цьому, якщо збільшувати кількість потоків, то навантаження зростає не так сильно, та Transaction Rate теж \
Тому середній час відповіді стає вище

Результати статистики по запитам:

```
Mongo Concurrency 5:
Lifting the server siege...
Transactions:                  10195 hits
Availability:                 100.00 %
Elapsed time:                  90.14 secs
Data transferred:             130.22 MB
Response time:                  0.04 secs
Transaction rate:             113.10 trans/sec
Throughput:                     1.44 MB/sec
Concurrency:                    4.98
Successful transactions:       10195
Failed transactions:               0
Longest transaction:            0.12
Shortest transaction:           0.03
 
Mongo Concurrency 20:
Transactions:                  11402 hits
Availability:                 100.00 %
Elapsed time:                  90.94 secs
Data transferred:             145.63 MB
Response time:                  0.16 secs
Transaction rate:             125.38 trans/sec
Throughput:                     1.60 MB/sec
Concurrency:                   19.97
Successful transactions:       11402
Failed transactions:               0
Longest transaction:            0.69
Shortest transaction:           0.03
 
Mongo Concurrency 50:
Transactions:                  11689 hits
Availability:                 100.00 %
Elapsed time:                  90.93 secs
Data transferred:             149.30 MB
Response time:                  0.39 secs
Transaction rate:             128.55 trans/sec
Throughput:                     1.64 MB/sec
Concurrency:                   49.80
Successful transactions:       11689
Failed transactions:               0
Longest transaction:            1.73
Shortest transaction:           0.03
 
ElastiSearch Concurrency 5:
Transactions:                   2354 hits
Availability:                 100.00 %
Elapsed time:                  90.96 secs
Data transferred:             192.79 MB
Response time:                  0.19 secs
Transaction rate:              25.88 trans/sec
Throughput:                     2.12 MB/sec
Concurrency:                    4.99
Successful transactions:        2354
Failed transactions:               0
Longest transaction:            0.70
Shortest transaction:           0.17
 
ElastiSearch Concurrency 20:
Lifting the server siege...
Transactions:                   2443 hits
Availability:                 100.00 %
Elapsed time:                  90.96 secs
Data transferred:             200.08 MB
Response time:                  0.74 secs
Transaction rate:              26.86 trans/sec
Throughput:                     2.20 MB/sec
Concurrency:                   19.90
Successful transactions:        2443
Failed transactions:               0
Longest transaction:            2.56
Shortest transaction:           0.18
 
ElastiSearch Concurrency 50:
Transactions:                   2462 hits
Availability:                 100.00 %
Elapsed time:                  90.94 secs
Data transferred:             201.63 MB
Response time:                  1.82 secs
Transaction rate:              27.07 trans/sec
Throughput:                     2.22 MB/sec
Concurrency:                   49.38
Successful transactions:        2462
Failed transactions:               0
Longest transaction:            5.57
Shortest transaction:           0.18

```




