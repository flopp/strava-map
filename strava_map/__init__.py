#!/usr/bin/env python

import flask
import logging
import stravalib

app = flask.Flask(__name__)
app.secret_key = 'this is my extremely secret key'
app.config.from_envvar('APP_CONFIG')
print(app.config)
port = 7123

logging.basicConfig(level=logging.INFO)


@app.route('/')
def homepage():
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    client = stravalib.client.Client(access_token=flask.session['access_token'])
    athlete = client.get_athlete()
    return flask.render_template('main.html', athlete=athlete.to_dict())


@app.route('/activities')
def activities():
    if 'access_token' not in flask.session:
        flask.abort(401)
    client = stravalib.client.Client(access_token=flask.session['access_token'])
    res = [item.to_dict() for item in client.get_activities()]
    return flask.jsonify(sorted(res, key=lambda a: a['start_date'], reverse=True))


@app.route('/login')
def login():
    client = stravalib.client.Client()
    auth_url = client.authorization_url(client_id=app.config['CLIENT_ID'],
                                        scope=None,
                                        redirect_uri='http://127.0.0.1:{}/auth'.format(port))
    return flask.render_template('login.html', auth_url=auth_url)


@app.route('/logout')
def logout():
    flask.session.pop('access_token')
    return flask.redirect(flask.url_for('homepage'))


@app.route('/auth')
def auth_done():
    code = flask.request.args.get('code', '')
    client = stravalib.client.Client()
    token = client.exchange_code_for_token(client_id=app.config['CLIENT_ID'],
                                           client_secret=app.config['CLIENT_SECRET'],
                                           code=code)
    flask.session['access_token'] = token
    return flask.redirect(flask.url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True, port=port)
