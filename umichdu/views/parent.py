from flask import Blueprint, render_template, jsonify

mod = Blueprint('parent', __name__, url_prefix='/parent')


@mod.route('/')
def index():
    return render_template('parent/index.html')
