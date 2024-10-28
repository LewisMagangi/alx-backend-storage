#!/usr/bin/env python3

import redis
import uuid

class Cache:
   def __init__(self):
      self.__redis = redis.Redis(host='localhost', port='6379', db=0)

      self.__redis.flushdb()

   def store(self, data):
      random_key = str(uuid.uuid4())
      self.__redis.set(random_key, data)
      return random_key
