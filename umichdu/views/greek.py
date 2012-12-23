from flask import Blueprint, render_template, jsonify

mod = Blueprint('greek', __name__, url_prefix='/greek')


@mod.route('/')
def index():
    return render_template('greek/index.html')
