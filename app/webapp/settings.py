# -*- coding: utf-8 -*-
import os

appConfig = {
    "DATABASE": str(os.path.join(os.getcwd(), 'app/webapp/data/flask_tut.db')),
    "SECRET_KEY": 'DfH89DdhcarM50X7R93P',
    "USERNAME": 'admin',
    "PASSWORD": 'default',
    "DEBUG": True
}
