from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from flask_openid import COMMON_PROVIDERS
from umichdu import oid
from umichdu.utils import requires_login, request_wants_json
from umichdu.database import db_session, User

mod = Blueprint('general', __name__)


@mod.route('/')
def index():
    return render_template('general/index.html')


@mod.route('/logout/')
def logout():
    if 'openid' in session:
        flash(u'Logged out')
        del session['openid']
    return redirect(request.referrer or url_for('general.index'))


@mod.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(url_for('general.index'))
    if 'cancel' in request.form:
        flash(u'Cancelled. The OpenID was not changed.')
        return redirect(oid.get_next_url())
    openid = request.values.get('openid')
    if not openid:
        openid = COMMON_PROVIDERS.get(request.args.get('provider'))
    if openid:
        return oid.try_login(openid, ask_for=['fullname', 'nickname'])
    error = oid.fetch_error()
    if error:
        flash(u'Error: ' + error)
    return render_template('general/login.html', next=oid.get_next_url())


@mod.route('/first-login/', methods=['GET', 'POST'])
def first_login():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('.login'))
    if request.method == 'POST':
        if 'cancel' in request.form:
            del session['openid']
            flash(u'Login was aborted')
            return redirect(url_for('general.login'))
        db_session.add(User(request.form['name'], session['openid']))
        db_session.commit()
        flash(u'Successfully created profile and logged in')
        return redirect(oid.get_next_url())
    return render_template('general/first_login.html',
                           next=oid.get_next_url(),
                           openid=session['openid'])


@mod.route('/profile/', methods=['GET', 'POST'])
@requires_login
def profile():
    name = g.user.name
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            flash(u'Error: a name is required')
        else:
            g.user.name = name
            db_session.commit()
            flash(u'User profile updated')
            return redirect(url_for('.index'))
    return render_template('general/profile.html', name=name)


@mod.route('/profile/change-openid/', methods=['GET', 'POST'])
@requires_login
@oid.loginhandler
def change_openid():
    if request.method == 'POST':
        if 'cancel' in request.form:
            flash(u'Cancelled. The OpenID was not changed.')
            return redirect(oid.get_next_url())
    openid = request.values.get('openid')
    if not openid:
        openid = COMMON_PROVIDERS.get(request.args.get('provider'))
    if openid:
        return oid.try_login(openid)
    error = oid.fetch_error()
    if error:
        flash(u'Error: ' + error)
    return render_template('general/change_openid.html',
                           next=oid.get_next_url())


@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    user = g.user or User.query.filter_by(openid=resp.identity_url).first()
    if user is None:
        return redirect(url_for('.first_login', next=oid.get_next_url(),
                                name=resp.fullname or resp.nickname))
    if user.openid != resp.identity_url:
        user.openid = resp.identity_url
        db_session.commit()
        flash(u'OpenID identity changed')
    else:
        flash(u'Successfully signed in')
    return redirect(oid.get_next_url())
