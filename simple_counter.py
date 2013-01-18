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

"""A module implementing a simple sharded counter."""


import random

from google.appengine.ext import ndb


NUM_SHARDS = 20


class SimpleCounterShard(ndb.Model):
    """Shards for the counter."""
    count = ndb.IntegerProperty(default=0)


def get_count():
    """Retrieve the value for a given sharded counter.

    Returns:
        Integer; the cumulative count of all sharded counters.
    """
    total = 0
    for counter in SimpleCounterShard.query():
        total += counter.count
    return total


@ndb.transactional
def increment():
    """Increment the value for a given sharded counter."""
    shard_string_index = str(random.randint(0, NUM_SHARDS - 1))
    counter = SimpleCounterShard.get_by_id(shard_string_index)
    if counter is None:
        counter = SimpleCounterShard(id=shard_string_index)
    counter.count += 1
    counter.put()
