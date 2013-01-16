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

"""A module implementing a general sharded counter."""


import random

from google.appengine.api import memcache
from google.appengine.ext import ndb


class GeneralCounterShardConfig(ndb.Model):
    """Tracks the number of shards for each named counter."""
    num_shards = ndb.IntegerProperty(default=20)


class GeneralCounterShard(ndb.Model):
    """Shards for each named counter."""
    count = ndb.IntegerProperty(default=0)


def get_count(name):
    """Retrieve the value for a given sharded counter.

    Args:
        name: The name of the counter.

    Returns:
        Integer; the cumulative count of all (sharded) counters for the given
            counter name.
    """
    total = memcache.get(name)
    if total is None:
        total = 0
        ancestor_key = ndb.Key(GeneralCounterShard, name)
        for counter in GeneralCounterShard.query(ancestor=ancestor_key):
            total += counter.count
        memcache.add(name, total, 60)
    return total


def increment(name):
    """Increment the value for a given sharded counter.

    Args:
        name: The name of the counter.
    """
    config = GeneralCounterShardConfig.get_or_insert(name)
    _increment(name, config.num_shards)


@ndb.transactional
def _increment(name, num_shards):
    """Transactional helper to increment the value for a given sharded counter.

    Also takes a number of shards to determine which shard will be used.

    Args:
        name: The name of the counter.
        num_shards: How many shards to use.
    """
    index = random.randint(0, num_shards - 1)
    shard_key = ndb.Key(GeneralCounterShard, name, GeneralCounterShard, index)
    counter = shard_key.get()
    if counter is None:
        counter = GeneralCounterShard(key=shard_key)
    counter.count += 1
    counter.put()
    # does nothing if the key does not exist
    memcache.incr(name)


@ndb.transactional
def increase_shards(name, num_shards):
    """Increase the number of shards for a given sharded counter.

    Will never decrease the number of shards.

    Args:
        name: The name of the counter.
        num_shards: How many shards to use.
    """
    config = GeneralCounterShardConfig.get_or_insert(name)
    if config.num_shards < num_shards:
        config.num_shards = num_shards
        config.put()
