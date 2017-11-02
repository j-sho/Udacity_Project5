"""
This file is the top level file for the Item Catalog project and
uses the Flask framework.
This project allows users to add recipies to categories.
Users can also edit and delete their own items.
JSON endpoints are provided for recipies and item.
Authentication is handled by Google's OAuth api and Facebook.
This file contains routes and view functions.
"""
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash, make_response)
from flask import session as login_session
from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from functools import wraps

import requests
import random
import string
import httplib2
import json

from models.login import (upgrade_to_credentials, token_info,
                          is_already_logged_in, get_user_info,
                          update_login_session, welcome_output,
                          fbtoken_info, fbget_user_info,
                          fbupdate_login_session)

from models.decorators import (login_required, category_exist,
                               recipe_exist, user_is_owner_category,
                               user_is_owner_recipe, category_empty,
                               authorised_make_like, getUserID,
                               getUserInfo)

from models.logout import (g_del_login, fb_del_login)

from db.database_funcion import (db_create_session, db_createUser,
                                 db_likesCount, db_showCategories,
                                 db_showCategory, db_createCategory,
                                 db_deleteCategory, db_editCategory,
                                 db_showRecipes, db_showRecipeItem,
                                 db_editRecipeItem, db_deleteRecipeItem,
                                 db_createRecipeItem, db_likesAdd)

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Food Recipes App"

session = db_create_session()

@app.route('/categories/<int:category_id>/recipes/JSON')
def restaurantMenuJSON(category_id):
    '''
      JSON APIs to view Recipes Information of specified category
    '''
    category = db_showCategory(session, category_id)
    items = db_showRecipes(session, category_id)
    return jsonify(RecipeItems=[i.serialize for i in items])


@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/JSON')
def menuItemJSON(category_id, recipe_id):
    '''
      JSON APIs to view Recipe Information
    '''
    recipe_Item = db_showRecipeItem(session, recipe_id)
    return jsonify(Recipe_Item=recipe_Item.serialize)


# WELCOME PAGE

@app.route('/')
def welcomePage():
    '''
      Render welcome page template
    '''
    return render_template('welcome.html')

# LOGIN

@app.route('/login')
def showLogin():
    '''
      Render login page via Facebook or Google+
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# FACEBOOK CONNECT


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    '''
      Gathers data from Facebook Sign in API and places it inside
      login_session variable
    '''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    data = fbtoken_info(access_token)
    token = 'access_token=' + data['access_token']

    user_info = fbget_user_info(token)

    fbupdate_login_session(login_session, user_info, token)

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = db_createUser(session, login_session)
    login_session['user_id'] = user_id


    welcome_output(login_session)
    print "fbconnect done!"
    return "OK"

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?' \
          'access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

# GOOGLE CONNECT

@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    '''
      Gathers data from Facebook Sign in API and places it inside
      login_session variable
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        # Obtain authorization code
    code = request.data

    try:
        credentials = upgrade_to_credentials(code)
    except FlowExchangeError:
        response = make_response(
          json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

      # Check that the access token is valid.
    access_token_info = token_info(credentials.access_token)

      # If there was an error in the access token info, abort.
    if access_token_info.get('error') is not None:
        response = make_response(json.dumps(access_token_info.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

      # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if access_token_info['user_id'] != gplus_id:
        response = make_response(
          json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

        # Verify that the access token is valid for this app.
    if access_token_info['issued_to'] != CLIENT_ID:
        response = make_response(
          json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    if is_already_logged_in(login_session):
        response = make_response(json.dumps('Current user is already connected.'),
                                     200)
        response.headers['Content-Type'] = 'application/json'
        return response

    user_info = get_user_info(credentials.access_token)
    update_login_session(login_session, credentials, gplus_id, user_info)
    print ("login_session['username'] %s" %login_session['username'])

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = db_createUser(session, login_session)
    login_session['user_id'] = user_id
    print ("login_session['user_id'] %s" %login_session['user_id'])
    welcome_output(login_session)
    print "gconnect done!"
    return "OK"


# GOOGLE DISCONNECT

@app.route('/gdisconnect')
def gdisconnect():
    '''
      Log out from Google+ account
    '''
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    '''
      Logout and delete data from login_session variable
    '''
    if 'provider' in login_session:
        print ("LOGIN PROVIDER %s" %login_session['provider'])
        if 'provider' in login_session and login_session['provider'] == 'google':
            print ("IM IN GOOGLE DISCONECT")
            gdisconnect()
            g_del_login(login_session)
        if 'provider' in login_session and login_session['provider'] == 'facebook':
            print ("IM IN FACEBOOK DISCONECT")
            fbdisconnect()
            fb_del_login(login_session)
        flash("You have successfully been logged out.")
        return redirect(url_for('welcomePage'))
    else:
        flash("You were not logged in")
        return redirect(url_for('welcomePage'))


# WEB PAGES

@app.route('/categories')
def showCategory():
    '''
      Check if user is loged in and render categories page
    '''
    categories = db_showCategories(session)
    if 'username' not in login_session:
        return render_template('categoriespublic.html', category=categories)
    else:
        return render_template('categories.html', category=categories,
                                user=login_session['username'],
                                userImage=login_session['picture'])

@app.route('/categories/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    '''
      Check if user is loged in and create new category in database
    '''
    if request.method == 'POST':
        category_name = request.form['name']
        category_picture = request.form['picture']
        userID = getUserID(login_session['email'])
        newCategory = db_createCategory(session, category_name, category_picture, userID)
        return redirect(url_for('showCategory'))
    else:
        return render_template('newCategory.html', user=login_session['username'],
                               userImage=login_session['picture'])


@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
@category_exist
@category_empty
@user_is_owner_category
def deleteCategory(category_id):
    categoryToDelete = db_showCategory(session, category_id)
    if request.method == 'POST':
        db_deleteCategory(session, category_id)
        return redirect(url_for('showCategory'))
    else:
        return render_template('deleteCategory.html',
                               category=categoryToDelete,
                               user=login_session['username'],
                               userImage=login_session['picture'])

@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
@category_exist
@user_is_owner_category
def editCategory(category_id):
    '''
      Check if user is loged in and if he is a owner of category,
      and edit data of category in database
    '''
    editedCategory = db_showCategory(session, category_id)
    if request.method == 'POST':
        category_name = request.form['name']
        category_picture = request.form['picture']
        db_editCategory(session, category_id, category_name, category_picture)
        return redirect(url_for('showCategory'))
    else:
        return render_template('editCategory.html', category=editedCategory,
                               user=login_session['username'],
                               userImage=login_session['picture'])



@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/recipes/')
def showRecipe(category_id):
    '''
      Render page with recipies for specific category
    '''
    category = db_showCategory(session, category_id)
    items = db_showRecipes(session, category_id)
    if 'username' not in login_session:
        return render_template('publicrecipe.html', items=items, category=category)
    else:
        return render_template('recipe.html', items=items, category=category,
                               user=login_session['username'],
                               userImage=login_session['picture'])

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/')
@recipe_exist
def showRecipeItem(category_id, recipe_id):
    '''
      Render page with concrete recipe
    '''
    item = db_showRecipeItem(session, recipe_id)
    creator = getUserInfo(item.user_id)
    ingridientsArray = item.ingredients.split("\n")
    likesAll = db_likesCount(session, recipe_id)
    descriptionArray = item.description.split("\n")
    if 'username' not in login_session:
        return render_template('recipeitempublic.html', item=item,
                               creator=creator, ingridients=ingridientsArray,
                               description=descriptionArray)
    else:
        return render_template('recipeitem.html', item=item,
                               category_id=category_id,
                               creator=creator, ingridients=ingridientsArray,
                               description=descriptionArray,
                               user=login_session['username'],
                               userImage=login_session['picture'],
                               likes=likesAll)

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/edit',
           methods=['GET', 'POST'])
@login_required
@recipe_exist
@user_is_owner_recipe
def editRecipeItem(category_id, recipe_id):
    '''
      Check if user is loged in and if he is a owner of recipe,
      and edit data of recipe in database
    '''
    editedItem = db_showRecipeItem(session, recipe_id)
    if request.method == 'POST':
        recipe_name = request.form['name']
        recipe_picture = request.form['picture']
        recipe_description = request.form['description']
        recipe_ingredients = request.form['ingredients']
        recipe_prep_time = request.form['prep_time']
        db_editRecipeItem(session, category_id, recipe_id, recipe_name,
                          recipe_picture, recipe_description, recipe_ingredients,
                          recipe_prep_time)
        return redirect(url_for('showRecipe',
                                category_id=editedItem.category_id))
    else:
        return render_template('editrecipeitem.html', category_id=category_id,
                               recipe_id=recipe_id, item=editedItem,
                               user=login_session['username'],
                               userImage=login_session['picture'])

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/delete',
           methods=['GET', 'POST'])
@login_required
@recipe_exist
@user_is_owner_recipe
def deleteRecipeItem(category_id, recipe_id):
    '''
      Check if user is loged in and if he is a owner of recipe,
      and delete recipe from database
    '''
    deletedItem = db_showRecipeItem(session, recipe_id)
    if request.method == 'POST':
        db_deleteRecipeItem(session, category_id, recipe_id)
        return redirect(url_for('showRecipe',
                                category_id=deletedItem.category_id))
    else:
        return render_template('deleteRecipe.html', category_id=category_id,
                               recipe_id=recipe_id, item=deletedItem,
                               user=login_session['username'],
                               userImage=login_session['picture'])

@app.route('/categories/<int:category_id>/recipes/new',
           methods=['GET', 'POST'])
@login_required
def newRecipeItem(category_id):
    '''
      Check if user is loged in create recipe in database
    '''
    if request.method == 'POST':
        recipe_name = request.form['name']
        recipe_picture = request.form['picture']
        recipe_description = request.form['description']
        recipe_ingredients = request.form['ingredients']
        recipe_prep_time = request.form['prep_time']
        user_id = getUserID(login_session['email'])
        db_createRecipeItem(session, user_id, category_id, recipe_name, recipe_picture,
                            recipe_description, recipe_ingredients,
                            recipe_prep_time)
        return redirect(url_for('showRecipe',
                                category_id=category_id))
    else:
        return render_template('newrecipeitem.html', category_id=category_id,
                               user=login_session['username'],
                               userImage=login_session['picture'])

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/like',
           methods=['GET', 'POST'])
@login_required
@authorised_make_like
def likesAdd(category_id, recipe_id):
    '''
      Check if user was already put his like and if he is a owner of recipe,
      and if no, add like to database
    '''
    recipeArray = db_showRecipeItem(session, recipe_id)
    db_likesAdd(session, login_session, recipe_id)
    return redirect(url_for('showRecipeItem',
                            category_id=category_id,
                            recipe_id=recipe_id))




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
