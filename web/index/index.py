from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return 'hello index'
