from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yahelzaken:1234@localhost/glycemic_index'
db = SQLAlchemy(app)

from aux_files import routes

