import json
import math
from app import app, db
from app.lib.helper import FormError, fillErrorDictionary, get_all_food_categories
from flask import redirect, render_template, request, session, flash

from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/recipes")
def recipe_list_page():
    # Get All Categories
    categories = get_all_food_categories()

    # Total Per Page
    items_per_page = 6

    # For Page Query
    page = request.args.get('page')
    page = int(page) if (page and int(page) > 0) else 1
    offset = 0 if page == 1 else (page - 1) * items_per_page + 1

    # Category Query
    category_query = request.args.get('category')
    category = category_query if not (
        category_query == None or category_query == "") else ""
    
    # Recipe Title Query
    reci_search_query = request.args.get('search_query')
    search_query = reci_search_query if not (
        reci_search_query == None or reci_search_query == "") else ""

    total_query = "SELECT COUNT(id) as total_row FROM recipes "
    
    if (search_query and category):
        total_query += " WHERE recipes.title LIKE ? AND recipes.category_id = ?"
        total_execute = db.execute(total_query, "%" + search_query + "%", category)
    elif search_query: 
        total_query += " WHERE recipes.title LIKE ? "
        total_execute = db.execute(total_query, "%" + search_query + "%")
    elif category:
        total_query += " WHERE recipes.category_id = ? "
        total_execute = db.execute(total_query, category)
    else:
        total_execute = db.execute(total_query)

    total_rows = total_execute[0]

    # search_query = ""

    selector = "recipes.id, recipes.image, recipes.title, users.id as user_id, users.image_avatar as user_image_avatar, users.name as user_name "
    recipe_query = "SELECT " + selector
    recipe_query += " FROM recipes "
    recipe_query += " INNER JOIN users on users.id = recipes.user_id "

    if (search_query and category):
        recipe_query += " WHERE recipes.title LIKE ?  AND recipes.category_id = ? "
    elif category:
        recipe_query += " WHERE recipes.category_id = ? "
    elif search_query:
        recipe_query += " WHERE recipes.title LIKE ? "

    recipe_query += " ORDER BY recipes.id DESC LIMIT 6 OFFSET " + str(offset)

    # Executing
    if (search_query and category):
        recipes = db.execute(recipe_query, "%" + search_query + "%", category)
    elif search_query:
        recipes = db.execute(recipe_query, "%" + search_query + "%")
    elif category:
        recipes = db.execute(recipe_query, category)
    else:
        recipes = db.execute(recipe_query)

    # Total Page
    total_page = math.ceil(total_rows['total_row'] / items_per_page)

    return render_template("recipe/index.html",
                           recipes=recipes, page=page, total_page=total_page, categories=categories, category=category, search_query=search_query)


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
