from flask import Flask
from . import index


app = Flask(__name__)

app.register_blueprint(index.bp)
app.add_url_rule('/', endpoint='index')
