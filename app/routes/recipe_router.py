import json
from app import app, db
from app.lib.helper import FormError, fillErrorDictionary
from flask import redirect, render_template, request, session, flash

from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/recipes")
def recipe_list_page():

    recipe_query = "SELECT recipes.id, recipes.image, recipes.title, "
    recipe_query += " users.id as user_id, users.image_avatar as user_image_avatar, users.name as user_name "
    recipe_query += " FROM recipes "
    recipe_query += " INNER JOIN users on users.id = recipes.user_id "
    recipe_query += " ORDER BY recipes.id DESC LIMIT 20 OFFSET 0"

    recipes = db.execute(recipe_query)

    return render_template("recipe/index.html", recipes=recipes)

@app.route("/recipes/<recipe_id>")
def recpie_detail_show_page(recipe_id):
    recipe_query = "SELECT recipes.id, recipes.image, recipes.title, recipes.ingredients, recipes.youtube_link, recipes.steps, "
    recipe_query += " categories.id as category_id, categories.title as category_title, "
    recipe_query += " users.id as user_id, users.image_avatar as user_image_avatar, users.name as user_name "
    recipe_query += " FROM recipes INNER JOIN categories on categories.id = recipes.category_id "
    recipe_query += " INNER JOIN users on users.id = recipes.user_id "
    recipe_query += " WHERE recipes.id = ?"
    recipe_exec = db.execute(recipe_query, recipe_id)
    recipe = recipe_exec[0] if len(recipe_exec) > 0 else None
    
    if not recipe is None:
        recipe["ingredients"] = json.loads(recipe["ingredients"]) 
        recipe["steps"] = json.loads(recipe["steps"]) 

    return render_template("recipe/recipe_detail.html", recipe=recipe)