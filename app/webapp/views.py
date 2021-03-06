# -*- coding: utf-8 -*-
from flask import flash, session, redirect, render_template, request, \
    url_for, abort

import dbconnector as dbc  # db methods
from webapp import app  # reference to app instance


# VIEWS
@app.route('/tutorial/')
def show_entries():
    db = dbc.get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('tutorial/show_entries.html', entries=entries)


@app.route('/tutorial/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = dbc.get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/tutorial/login', methods=['GET', 'POST'])
def tutorial_login():
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
def tutorial_logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# main page of application
@app.route('/')
def show_dashboard():
    ctx = {
        'news': {
            'new_accounts': 2,
            'tree_request': 6,
            'support': 0
        },
        'notifications': [
            ('Notification #3', '1 minute'),
            ('Notification #2', '7 minute'),
            ('Notification #1', '31 minute')
        ],
        'graphic': True
    }
    return render_template('dashboard.html', ctx=ctx)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/layout')
def show_layout():
    return render_template('layout.html')


@app.route('/tree/')
def graphic_tree():
    return render_template('tree/display-edit.html')


@app.route('/tree/historic')
def show_timeline():
    ctx = {
        'notifications': [
            ('Notification #3', '1 minute'),
            ('Notification #2', '7 minute'),
            ('Notification #1', '31 minute')
        ]
    }
    return render_template('tree/historic.html', ctx=ctx)


@app.route('/tree/approvals')
def show_approvals():
    return render_template('tree/approval.html')
