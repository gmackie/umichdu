from flask import Flask, session, g, render_template
from flask_openid import OpenID

app = Flask(__name__)
app.config.from_object('websiteconfig')

from umichdu.openid_auth import DatabaseOpenIDStore
oid = OpenID(app, store_factory=DatabaseOpenIDStore)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.before_request
def load_current_user():
    g.user = User.query.filter_by(openid=session['openid']).first() \
        if 'openid' in session else None


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


from umichdu.views import general
from umichdu.views import parent
from umichdu.views import greek
from umichdu.views import chapter
from umichdu.views import history
from umichdu.views import recruit
app.register_blueprint(general.mod)
app.register_blueprint(parent.mod)
app.register_blueprint(greek.mod)
app.register_blueprint(chapter.mod)
app.register_blueprint(history.mod)
app.register_blueprint(recruit.mod)

from umichdu.database import User, db_session
from umichdu import utils

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
app.jinja_env.filters['displayopenid'] = utils.display_openid
