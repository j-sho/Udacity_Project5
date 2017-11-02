"""
This file contains convenience/helper functions for loging out.
Function for fbdisconnect() and gdisconnect()
could be found in application.py.
The intent is thet functions to be clearer by using these helper functions.
"""
import httplib2

def g_del_login(login_session):
    del login_session['gplus_id']
    del login_session['credentials']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']

def fb_del_login(login_session):
    del login_session['facebook_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']
