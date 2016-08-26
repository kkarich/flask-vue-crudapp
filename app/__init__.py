from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# init DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# set default route. this will be used to serve the vue.js application
@app.route('/')
def index():
    return render_template('index.html')

# import the person module. This adds routes for JSON API
import person


