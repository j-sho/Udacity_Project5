"""
This file contains decorators and additional function:
- to check if user was loged in
- to chesk if category and recipe exist
- to chesk if user is owner of recipe o category
and has permission to make changes
- to chesk if user can make like to recipe
"""

from flask import redirect
from flask import session as login_session
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from db.database_setup import (Base, User, Category,
                               Recipe, Likes)

from db.database_funcion import (db_showCategory, db_showRecipeItem,
                                 db_showRecipes, db_likes)

engine = create_engine('sqlite:///recipesbycategory.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    return decorator

def category_exist(func):
    @wraps(func)
    def decorator(category_id, *args, **kwargs):
        category = db_showCategory(session, category_id)
        if category:
            return func(category_id, *args, **kwargs)
        else:
            output = ''
            output += '<h2>Sorry, there is no such category!</h2>'
            return output
    return decorator


def recipe_exist(func):
    @wraps(func)
    def decorator(category_id, recipe_id, *args, **kwargs):
        recipe = db_showRecipeItem(session, recipe_id)
        if recipe:
            return func(category_id, recipe_id, *args, **kwargs)
        else:
            output = ''
            output += '<h2>Sorry, there is no such recipe!</h2>'
            return output
    return decorator


def user_is_owner_category(func):
    @wraps(func)
    def decorator(category_id, *args, **kwargs):
        item = db_showCategory(session, category_id)
        creator = getUserInfo(item.user_id)
        print (func)
        if creator.name != login_session['username']:
            return "<script>function myFunction() {alert('You are not " \
                   "authorized to edit and delete, as you are not the owner.'" \
                   ");}</script><body onload='myFunction()''>"
        else:
            return func(category_id, *args, **kwargs)
    return decorator

def user_is_owner_recipe(func):
    @wraps(func)
    def decorator(category_id, recipe_id, *args, **kwargs):
        item = db_showRecipeItem(session, recipe_id)
        creator = getUserInfo(item.user_id)
        if creator.name != login_session['username']:
            return "<script>function myFunction() {alert('You are not authorized " \
               "to edit and delete, as you are not the owner.')"\
               ";}</script><body onload='myFunction()''>"
        else:
            return func(category_id, recipe_id, *args, **kwargs)
    return decorator

def category_empty(func):
    @wraps(func)
    def decorator(category_id, *args, **kwargs):
        print ("IM HERE")
        checkIfRecipes = db_showRecipes(session, category_id)
        print ("RECIPE %s" %checkIfRecipes)
        if checkIfRecipes:
            print ("IM HERE 2")
            return "<script>function emptyCheck() {alert('You can't delete " \
                "category with recipes!');}</script><body onload='emptyCheck()''>"
        else:
            print ("IM HERE 3")
            return func(category_id, *args, **kwargs)
    return decorator


def authorised_make_like(func):
    @wraps(func)
    def decorator(category_id, recipe_id, *args, **kwargs):
        recipe = db_showRecipeItem(session, recipe_id)
        checkIfLike = db_likes(session, login_session, recipe_id)
        if getUserInfo(recipe.user_id).name != login_session['username']:
            if not checkIfLike:
                return func(category_id, recipe_id, *args, **kwargs)
            else:
                return "<script>function myFunction() {alert('You already " \
                "put yout like!');}</script><body onload='myFunction()''>"
        else:
            return "<script>function myFunction() {alert('You cant " \
                "like your recipe!');}</script><body onload='myFunction()''>"
    return decorator


def getUserID(email):
    '''
      Return user id according to email provided
    '''
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    '''
      Return user name according to user id
    '''
    user = session.query(User).filter_by(id=user_id).first()
    return user
