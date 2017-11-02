from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Recipe

engine = create_engine('sqlite:///recipesbycategory.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Categories
category1 = Category(user_id=1, name='Appetizers and Snacks')

session.add(category1)
session.commit()

recipeItem1 = Recipe(user_id=1, name="Strawberry Bruschetta", description="1) Preheat your oven's broiler. Spread a thin layer of butter on each slice of bread. Arrange bread slices in a single layer on a large baking sheet. <br>2) Place bread under the broiler for 1 to 2 minutes, just until lightly toasted. Spoon some chopped strawberries onto each piece of toast, then sprinkle sugar over the strawberries. <br> 3) Place under the broiler again until sugar is caramelized, 3 to 5 minutes. Serve immediately.",
                     ingredients="24 slices French baguette;<br>1 tablespoon butter, softened;<br>2 cups chopped fresh strawberries;<br>1/4 cup white sugar, or as needed;", prep_time="15m", category=category1, picture="https://pbs.twimg.com/media/C-ldyjYUQAApMDk.jpg")

session.add(recipeItem1)
session.commit()

recipeItem2 = Recipe(user_id=1, name="Strawberry Bruschetta", description="1) Preheat your oven's broiler. Spread a thin layer of butter on each slice of bread. Arrange bread slices in a single layer on a large baking sheet. <br>2) Place bread under the broiler for 1 to 2 minutes, just until lightly toasted. Spoon some chopped strawberries onto each piece of toast, then sprinkle sugar over the strawberries. <br> 3) Place under the broiler again until sugar is caramelized, 3 to 5 minutes. Serve immediately.",
                     ingredients="24 slices French baguette;<br>1 tablespoon butter, softened;<br>2 cups chopped fresh strawberries;<br>1/4 cup white sugar, or as needed;", prep_time="15m", category=category1, picture="https://pbs.twimg.com/media/C-ldyjYUQAApMDk.jpg")

session.add(recipeItem2)
session.commit()

recipeItem3 = Recipe(user_id=1, name="Strawberry Bruschetta", description="1) Preheat your oven's broiler. Spread a thin layer of butter on each slice of bread. Arrange bread slices in a single layer on a large baking sheet. <br>2) Place bread under the broiler for 1 to 2 minutes, just until lightly toasted. Spoon some chopped strawberries onto each piece of toast, then sprinkle sugar over the strawberries. <br> 3) Place under the broiler again until sugar is caramelized, 3 to 5 minutes. Serve immediately.",
                     ingredients="24 slices French baguette;<br>1 tablespoon butter, softened;<br>2 cups chopped fresh strawberries;<br>1/4 cup white sugar, or as needed;", prep_time="15m", category=category1, picture="https://pbs.twimg.com/media/C-ldyjYUQAApMDk.jpg")

session.add(recipeItem3)
session.commit()

recipeItem4 = Recipe(user_id=1, name="Strawberry Bruschetta", description="1) Preheat your oven's broiler. Spread a thin layer of butter on each slice of bread. Arrange bread slices in a single layer on a large baking sheet. <br>2) Place bread under the broiler for 1 to 2 minutes, just until lightly toasted. Spoon some chopped strawberries onto each piece of toast, then sprinkle sugar over the strawberries. <br> 3) Place under the broiler again until sugar is caramelized, 3 to 5 minutes. Serve immediately.",
                     ingredients="24 slices French baguette;<br>1 tablespoon butter, softened;<br>2 cups chopped fresh strawberries;<br>1/4 cup white sugar, or as needed;", prep_time="15m", category=category1, picture="https://pbs.twimg.com/media/C-ldyjYUQAApMDk.jpg")

session.add(recipeItem4)
session.commit()

category2 = Category(user_id=1, name='Bread Recipes')

session.add(category2)
session.commit()

recipeItem2 = Recipe(user_id=1, name="Chef John's Buttermilk Biscuits", description="Preheat oven to 425 degrees F (220 degrees C).<br>Line a baking sheet with a silicone baking mat or parchment paper.<br>Cut butter into flour mixture with a pastry blender until the mixture resembles coarse crumbs, about 5 minutes.<br>Make a well in the center of butter and flour mixture. Pour in 3/4 cup buttermilk; stir until just combined.<br>Turn dough onto a floured work surface, pat together into a rectangle.<br>Fold the rectangle in thirds. Turn dough a half turn, gather any crumbs, and flatten back into a rectangle. Repeat twice more, folding and pressing dough a total of three times.<br>Roll dough on a floured surface to about 1/2 inch thick.<br>Cut out 12 biscuits using a 2 1/2-inch round biscuit cutter.<br>Transfer biscuits to the prepared baking sheet. Press an indent into the top of each biscuit with your thumb.<br>Brush the tops of biscuits with 2 tablespoons buttermilk.<br>Bake in the preheated oven until browned, about 15 minutes.",
                     ingredients="2 cups all-purpose flour;<br>2 teaspoons baking powder;<br>1 teaspoon salt;<br>1/4 teaspoon baking soda;<br>7 tablespoons unsalted butter, chilled in freezer and cut into thin slices;<br>3/4 cup cold buttermilk;<br>2 tablespoons buttermilk for brushing;", prep_time="35m", category=category2, picture="https://lh3.googleusercontent.com/3g2UnogIJxGiz94LM9jZhG9L8Xja6yb8APs_ZYgeczjJfCiMDYg2JJhFpQ6f6p9l5v1X=s151")

session.add(recipeItem2)
session.commit()


category3 = Category(user_id=1, name='Breakfast Recipes')

session.add(category3)
session.commit()

category4 = Category(user_id=1, name='Desserts')

session.add(category4)
session.commit()

category5 = Category(user_id=1, name='Drinks')

session.add(category5)
session.commit()

category6 = Category(user_id=1, name='Main Dishes')

session.add(category6)
session.commit()

category7 = Category(user_id=1, name='Salad Recipes')

session.add(category7)
session.commit()

print "added resipe items!"

