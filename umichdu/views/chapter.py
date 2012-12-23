from flask import Blueprint, render_template, jsonify

mod = Blueprint('chapter', __name__, url_prefix='/chapter')


@mod.route('/')
def index():
    return render_template('chapter/index.html')


@mod.route('/brothers/')
def brothers():
	return render_template('chapter/brothers.html')


@mod.route('/alumni/')
def alumni():
	return render_template('chapter/alumni.html')
