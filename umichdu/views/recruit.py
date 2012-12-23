from flask import Blueprint, render_template, jsonify

mod = Blueprint('recruit', __name__, url_prefix='/recruit')


@mod.route('/')
def index():
    return render_template('recruit/index.html')
