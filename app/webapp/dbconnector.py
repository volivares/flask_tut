# -*- coding: utf-8 -*-
import sqlite3

from flask import g

from webapp import app


# DATABASE METHODS
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new connection if there is none yet for the current
    application context
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('../schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
