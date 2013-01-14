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

"""A simple application that demonstrates sharding counters.

Uses sharded counters to achieve higher throughput.

Demonstrates:
   * Sharding - Sharding a counter into N random pieces
   * Memcache - Using memcache to cache the total counter value in
                general_counter.
"""

import webapp2
from webapp2_extras import jinja2

import general_counter
import simple_counter


class CounterHandler(webapp2.RequestHandler):
  """Handles displaying the values of the counters
  and requests to increment either counter.
  """

  @webapp2.cached_property
  def jinja2(self):
    """Cached property holding a Jinja2 instance."""
    return jinja2.get_jinja2(app=self.app)

  def render_response(self, template, **context):
    """Use Jinja2 instance to render template and write to output.

    Args:
      template: filename (relative to $PROJECT/templates) that we are
        rendering.
      context: keyword arguments corresponding to variables in template.
    """
    rendered_value = self.jinja2.render_template(template, **context)
    self.response.write(rendered_value)

  def get(self):
    simpletotal = simple_counter.get_count(),
    generaltotal = general_counter.get_count('FOO')
    self.render_response('counter.html', simpletotal=simpletotal,
                         generaltotal=generaltotal)

  def post(self):
    counter = self.request.get('counter')
    if counter == 'simple':
      simple_counter.increment()
    else:
      general_counter.increment('FOO')
    self.redirect("/")


APPLICATION = webapp2.WSGIApplication(
    [('/', CounterHandler)],
    debug=True)
