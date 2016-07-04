#!/usr/bin/env python

import os
import webapp
import unittest
import tempfile


class AppTutorialTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, webapp.app.config['DATABASE'] = tempfile.mkstemp()
        webapp.app.config['TESTING'] = True
        self.app = webapp.app.test_client()
        with webapp.app.app_context():
            webapp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(webapp.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/tutorial/')
        assert b'No entries here so far' in rv.data

    def tuto_login(self, username, password):
        return self.app.post(
            '/tutorial/login',
            data=dict(
                username=username,
                password=password),
            follow_redirects=True)

    def tuto_logout(self):
        return self.app.get(
            '/tutorial/logout',
            follow_redirects=True)

    def test_login_logout(self):
        rv = self.tuto_login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.tuto_logout()
        assert 'You were logged out' in rv.data
        rv = self.tuto_login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.tuto_login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.tuto_login('admin', 'default')
        rv = self.app.post('/tutorial/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()
