"""
This file contains the SQL Alchemy classes used to define the database
tables.
The database tables 'user', 'category', 'recipe' and 'like' are defined here.
Functions to query or modify the database could be found in
db/database_access.py.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    picture = Column(String(250))
    description = Column(String(250), nullable=False)
    ingredients = Column(String(250), nullable=False)
    prep_time = Column(String(8))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'picture': self.picture,
           'description': self.description,
           'ingredients': self.ingredients,
           'prep_time': self.prep_time,
           'category_id': self.category_id,
           'user_id': self.user_id,
       }

class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship(Recipe)




engine = create_engine('sqlite:///recipesbycategory.db')


Base.metadata.create_all(engine)
