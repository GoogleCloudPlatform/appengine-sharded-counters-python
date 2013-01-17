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

Counters can be sharded to achieve higher throughput.

Demonstrates:
   * Sharding - Sharding a counter into N random pieces.
   * Memcache - Using memcache to cache the total counter value in
                general_counter.
"""


import webapp2
from webapp2_extras import jinja2

import general_counter
import simple_counter


DEFAULT_COUNTER_NAME = 'FOO'


class CounterHandler(webapp2.RequestHandler):
    """Handles displaying counter values and requests to increment a counter.

    Uses a simple and general counter and allows either to be updated.
    """

    @webapp2.cached_property
    def jinja2(self):
        """Cached property holding a Jinja2 instance.

        Returns:
            A Jinja2 object for the current app.
        """
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
        """GET handler for displaying counter values."""
        simple_total = simple_counter.get_count()
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response('counter.html', simple_total=simple_total,
                             general_total=general_total)

    def post(self):
        """POST handler for updating a counter which is specified in payload."""
        counter = self.request.get('counter')
        if counter == 'simple':
            simple_counter.increment()
        else:
            general_counter.increment(DEFAULT_COUNTER_NAME)
        self.redirect('/')


APPLICATION = webapp2.WSGIApplication([('/', CounterHandler)],
                                      debug=True)
