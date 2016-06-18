# -*- coding: utf-8 -*-

import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

from webapp.settings import appConfig

############################## APP INSTANCE ####################################
app = Flask(__name__)
app.config.update(appConfig)

import dbconnector as dbc # db methods
import webapp.views

########################## ADITIONAL CLI COMMANDS ##############################
@app.cli.command('initdb')
def initdb_command():
	"""Initializes the database
	for windows run:
		set FLASK_APP=app\webapp\__init__.py
		set FLASK_DEBUG=1
		flask initdb
	"""
	print appConfig['DATABASE']
	dbc.init_db()
	print 'Initialized the database.'

@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the request"""
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()

