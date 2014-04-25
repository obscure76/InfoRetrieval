from requests_oauthlib import OAuth2Session

from flask import Flask, request, redirect, session, url_for
#from flask.json import jsonify

# This information is obtained upon registration of a new GitHub
client_id = '32b67d9db6a9c7c7fd62'
client_secret = '4c15f439c7288a0a4de840b2c030474852fec0f2'
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

@app.route("/login")
def login():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    return github.get('https://api.github.com/user').json()
