"""
This file contains convenience/helper functions for logging in and
logging out functions gconnect() and fbconnect()
found in application.py.
The intent is for the gconnect() and gdisconnect() functions to be
clearer by using these helper functions.
"""


from oauth2client.client import flow_from_clientsecrets
from flask import flash
import httplib2
import json
import requests

# GOOGLE+

def upgrade_to_credentials(code):
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
    return credentials


def token_info(access_token):
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    return result


def is_already_logged_in(login_session):
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    return stored_credentials is not None and stored_gplus_id is not None


def get_user_info(access_token):
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    return answer.json()


def update_login_session(login_session, credentials, gplus_id, user_info):
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    login_session['username'] = user_info['name']
    login_session['picture'] = user_info['picture']
    login_session['email'] = user_info['email']
    login_session['id'] = 'GOOGLE_ID_' + user_info['id']
    login_session['provider'] = 'google'

def welcome_output(login_session):
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;' \
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# FACEBOOK
def fbtoken_info(access_token):
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
      'web']['app_id']
    app_secret = json.loads(
            open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/v2.8/oauth/access_token?' \
        'grant_type=fb_exchange_token&client_id=%s&client_secret=%s&' \
        'fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    return data

def fbget_user_info(token):
    url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "API JSON result: %s" % result
    data = json.loads(result)
    return data

def fbupdate_login_session(login_session, user_info, token):
    login_session['provider'] = 'facebook'
    login_session['username'] = user_info["name"]
    login_session['email'] = user_info["email"]
    login_session['facebook_id'] = user_info["id"]
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token
    url = 'https://graph.facebook.com/v2.8/me/picture?%s&' \
        'redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]
