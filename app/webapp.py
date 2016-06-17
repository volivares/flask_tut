# -*- coding: utf-8 -*-

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# create the application
app = Flask(__name__)
#app.config.from_object(__name__)

# load default config and override config from an environment variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'data/flask_tut.db'),
	SECRET_KEY='DfH89DdhcarM50X7R93P',
	USERNAME='admin',
	PASSWORD='dhcarM50X',
	DEBUG=True
))


def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()


@app.cli.command('initdb')
def initdb_command():
	"""Initializes the database
	for windows run:
		set FLASK_APP=app\webapp.py
		set FLASK_DEBUG=1
		flask initdb
	"""
	init_db()
	print 'Initialized the database.'


def get_db():
	"""Opens a new connection if there is none yet for the current 
	application context
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the request"""
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()

@app.route('/tutorial/')
def show_entries():
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc')
	entries = cur.fetchall()
	return render_template('tutorial/show_entries.html', entries=entries)

@app.route('/tutorial/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text) values (?, ?)',
		[request.form['title'], request.form['text']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/tutorial/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('tutorial/login.html', error=error)

@app.route('/tutorial/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()