#!/usr/bin/env python

import os
import webapp
import unittest
import tempfile


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, webapp.app.config['DATABASE'] = tempfile.mkstemp()
        webapp.app.config['TESTING'] = True
        self.app = webapp.app.test_client()
        with webapp.app.app_context():
            webapp.init_db()
