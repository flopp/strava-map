#!/usr/bin/env python

import flask
import logging
import stravalib
import os
import json

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

    return flask.render_template('main.html', athlete=load_athlete(), activities=load_activities())


def load_athlete():
    athlete_id = fetch_athlete_data()
    d = 'data/{}'.format(athlete_id)
    with open('{}/athlete.json'.format(d), 'r') as f:
        return json.load(f)


def load_activities():
    athlete_id = fetch_athlete_data()
    d = 'data/{}/activities/'.format(athlete_id)
    try:
        sub_dirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    except FileNotFoundError:
        return []
    activities = []
    for s in sub_dirs:
        with open('{}/data.json'.format(s), 'r') as f:
            data = json.load(f)
            activities.append(data)

    return sorted(activities, key=lambda a: a['start_date'], reverse=True)


def fetch_athlete_data():
    if 'athlete_id' not in flask.session:
        client = stravalib.client.Client(access_token=flask.session['access_token'])
        athlete = client.get_athlete()
        flask.session['athlete_id'] = athlete.id
        d = 'data/{}'.format(athlete.id)
        os.makedirs(d, exist_ok=True)
        with open('{}/athlete.json'.format(d), 'w') as f:
            json.dump(athlete.to_dict(), f, sort_keys=True, indent=4)
    return flask.session['athlete_id']


@app.route('/sync')
def sync():
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    athlete_id = fetch_athlete_data()
    client = stravalib.client.Client(access_token=flask.session['access_token'])

    d = 'data/{}/activities/'.format(athlete_id)
    os.makedirs(d, exist_ok=True)

    activities = client.get_activities()
    for activity in activities:
        d = 'data/{}/activities/{}'.format(athlete_id, activity.id)
        os.makedirs(d, exist_ok=True)
        with open('{}/data.json'.format(d), 'w') as f:
            json.dump(activity.to_dict(), f, sort_keys=True, indent=4)

    return flask.redirect(flask.url_for('homepage'))


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
    flask.session.pop('athlete_id')
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
