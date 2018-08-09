# -*- coding: utf-8 -*-
import random
import redis

r=redis.StrictRedis(host='192.168.123.105',port=6379, password='younglinuxer')
for i in range(100):
    r.set(i, random.randint(1,10000))
# a=[r.get(i) for i in range(100)]
# print a
