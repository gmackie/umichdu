from flask import Blueprint, render_template, jsonify

mod = Blueprint('history', __name__, url_prefix='/history')


@mod.route('/')
def index():
    return render_template('history/index.html')
