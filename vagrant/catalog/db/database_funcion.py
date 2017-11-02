"""
This file contains functions to access the database. These functions
are prefixed by 'db_' to emphasize that they query, update, or delete
objects in the database.
SQLAlchemy is used as the Object-Relational Manager.
Table/class definitions are contained in db/database_setup.py.
"""
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Recipe, Likes
from flask import flash
from sqlalchemy import and_

def db_create_session():
    engine = create_engine('sqlite:///recipesbycategory.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def db_createUser(session, login_session):
    '''
      Create new user in database by data provided in login session variable
    '''
    newUser = User(name=login_session['username'], email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def db_likesCount(session, recipe_id):
    '''
      Count all likes made for concrete recipe
    '''
    allLikes = session.query(Likes).filter_by(recipe_id=recipe_id).count()
    return allLikes

def db_showCategories(session):
    categories = session.query(Category).order_by(asc(Category.name))
    return categories

def db_showCategory(session, category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    return category

def db_createCategory(session, category_name, category_picture, userID):
    newCategory = Category(name=category_name,
                           picture=category_picture,
                           user_id=userID)
    session.add(newCategory)
    session.commit()
    return flash('New Category %s Successfully Created' % newCategory.name)

def db_deleteCategory(session, category_id):
    categoryToDelete = db_showCategory(session, category_id)
    session.delete(categoryToDelete)
    session.commit()
    return flash('%s Successfully Deleted' % categoryToDelete.name)

def db_editCategory(session, category_id, category_name, category_picture):
    editedCategory = db_showCategory(session, category_id)
    if category_name:
      editedCategory.name = category_name
    if category_picture:
      editedCategory.picture = category_picture
    session.add(editedCategory)
    session.commit()
    return flash('Category Successfully Edited %s' % editedCategory.name)

def db_showRecipes(session, category_id):
    items = session.query(Recipe).filter_by(
            category_id=category_id).all()
    return items

def db_showRecipeItem(session, recipe_id):
    item = session.query(Recipe).filter_by(id=recipe_id).first()
    return item

def db_editRecipeItem(session, category_id, recipe_id, recipe_name,
                      recipe_picture, recipe_description, recipe_ingredients,
                      recipe_prep_time):
    editedItem = db_showRecipeItem(session, recipe_id)
    if recipe_name:
        editedItem.name = recipe_name
    if recipe_picture:
        editedItem.picture = recipe_picture
    if recipe_description:
        editedItem.description = recipe_description
    if recipe_ingredients:
        editedItem.ingredients = recipe_ingredients
    if recipe_prep_time:
        editedItem.prep_time = recipe_prep_time
    session.add(editedItem)
    session.commit()
    return flash('Recipe was Successfully Edited')

def db_deleteRecipeItem(session, category_id, recipe_id):
    deletedItem = db_showRecipeItem(session, recipe_id)
    deletedItemLikes = session.query(Likes).filter_by(recipe_id=recipe_id).all()
    session.delete(deletedItem)
    for likes in deletedItemLikes:
        session.delete(likes)
    session.commit()
    return flash('Recipe Item Successfully Deleted')


def db_createRecipeItem(session, user_id, category_id, recipe_name, recipe_picture,
                        recipe_description, recipe_ingredients,
                        recipe_prep_time):
    newItem = Recipe(name=recipe_name,
                     picture=recipe_picture,
                     description=recipe_description,
                     ingredients=recipe_ingredients,
                     prep_time=recipe_prep_time,
                     category_id=category_id,
                     user_id=user_id)
    session.add(newItem)
    session.commit()
    return flash('New Recipe %s Item Successfully Created' % (newItem.name))

def db_likesAdd(session, login_session, recipe_id):
    newLike = Likes(user_id=login_session['username'], recipe_id=recipe_id)
    session.add(newLike)
    session.commit()
    return flash("Your's like successfully added")

def db_likes(session, login_session, recipe_id):
    userLike =session.query(Likes).filter(and_(Likes.recipe_id==recipe_id,
                      Likes.user_id==login_session['username'])).first()
    return userLike
