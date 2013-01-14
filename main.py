#!/usr/bin/env python
#
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

"""A simple application that demonstrates sharding counters
   to achieve higher throughput.

Demonstrates:
   * Sharding - Sharding a counter into N random pieces
   * Memcache - Using memcache to cache the total counter value in generalcounter.
"""

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import generalcounter
import simplecounter

class CounterHandler(webapp.RequestHandler):
  """Handles displaying the values of the counters
  and requests to increment either counter.
  """

  def get(self):
    template_values = {
      'simpletotal': simplecounter.get_count(),
      'generaltotal': generalcounter.get_count('FOO')
    }
    template_file = os.path.join(os.path.dirname(__file__), 'counter.html')
    self.response.out.write(template.render(template_file, template_values))

  def post(self):
    counter = self.request.get('counter')
    if counter == 'simple':
      simplecounter.increment()
    else:
      generalcounter.increment('FOO')
    self.redirect("/")


def main():
  application = webapp.WSGIApplication(
  [  
    ('/', CounterHandler),
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
  

