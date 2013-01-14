# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import db
import random

class SimpleCounterShard(db.Model):
  """Shards for the counter"""
  count = db.IntegerProperty(required=True, default=0)    

NUM_SHARDS = 20

def get_count():
  """Retrieve the value for a given sharded counter."""
  total = 0
  for counter in SimpleCounterShard.all():
    total += counter.count
  return total
    
def increment():
  """Increment the value for a given sharded counter."""
  def txn():
    index = random.randint(0, NUM_SHARDS - 1)
    shard_name = "shard" + str(index)
    counter = SimpleCounterShard.get_by_key_name(shard_name)
    if counter is None:
      counter = SimpleCounterShard(key_name=shard_name)
    counter.count += 1
    counter.put()
  db.run_in_transaction(txn)


