import math
import random
import time
import os
from redis.sentinel import Sentinel


# Connect to Sentinel
sentinel = Sentinel([(os.getenv('SENTINEL_ADDRESS'), 26379)], socket_timeout=0.1)

# Get a connection to the master
master = sentinel.master_for(os.getenv('SENTINEL_MASTER_NAME'), socket_timeout=0.1, decode_responses=True)

# Get a connection to a slave
slave = sentinel.slave_for(os.getenv('SENTINEL_MASTER_NAME'), socket_timeout=0.1, decode_responses=True)


def get_with_probabilistic_cache(function: callable, hash_key: str, beta: int = 1):
    is_cached = True

    def is_need_to_use_probabilistic_cache(expiry: int):
        expiry_timestamp = time.time() + expiry
        if (time.time() - delta * beta * math.log(random.uniform(0, 1))) >= expiry_timestamp:
            return True
        return False

    ttl = 0
    if res := slave.hmget(hash_key, ['value', 'delta']):
        ttl = slave.ttl(hash_key)
    value, delta = res

    if delta:
        delta = float(delta)

    if not value or is_need_to_use_probabilistic_cache(ttl):
        start = time.time()
        value = function()
        delta = time.time() - start

        master.hset(hash_key, mapping={'value': value, 'delta': delta})
        master.expire(hash_key, 60)
        is_cached = False

    return value, is_cached, ttl


def get_data():
    def hard_function(i: int):
        time.sleep(2)
        return i * 2
    random_number = random.randint(1, 3)

    result, is_cached, ttl = get_with_probabilistic_cache(lambda: hard_function(random_number),
                                                          f"cached_data:{random_number}")
    print(f'Result from redis: {result}, is cached: {is_cached}: ttl: {ttl}')


def main():
    get_data()


if __name__ == '__main__':
    main()
