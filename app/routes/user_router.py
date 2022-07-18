import json
import logging
import math
import os
from app import app, db
from flask import flash, jsonify, render_template, session, request, redirect
from app.lib.helper import FormError, check_image_file_valid, check_image_validator, fillErrorDictionary, fillOldRequest, get_all_food_categories, uuid_url64
from app.middleware.authentication import auth_required
from werkzeug.utils import secure_filename


@app.route("/user")
@auth_required
def user_index_page():
    return render_template("user/index.html")


@app.route("/user/profile", methods=["GET", "POST"])
@auth_required
def user_profile_page():
    errors = []
    errors_dict = {
        'name': '',
        'background_image': '',
        'status': '',
        'intro_text': '',
        'old_name': '',
        'old_background_image': '',
        'old_status': '',
        'old_intro_text': '',
    }

    # Default Background Image List
    user_id = session["user_id"]
    user_query = "SELECT name, image_avatar, background_image, status, intro_text, role_id FROM users WHERE id = ?"
    user = db.execute(user_query, user_id)
    default_bg_images = []
    for i in range(1, 8):
        default_bg_images.append("/img/background/default_" + str(i) + ".jpg")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_id = session["user_id"]
        user_query = "SELECT name, image_avatar, background_image, status, intro_text, role_id FROM users WHERE id = ?"
        user = db.execute(user_query, user_id)

        username = request.form.get("username")
        background_image = request.form.get("background_image")
        status = request.form.get("status")
        intro_text = request.form.get("intro_text")

        # Ensure username was submitted
        if not username:
            errors.append(
                FormError("username", "User name is required", username))

        # Ensure Background image is included
        if not background_image:
            errors.append(FormError("background_image",
                          "Background image is required", background_image))

        if len(errors) > 0:
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("user/profile.html", errors=errors_dict, user=user[0], default_bg_images=default_bg_images)

        updated_user_query = "UPDATE users SET name = ?, background_image = ?, status = ?, intro_text = ? WHERE id = ?"
        db.execute(updated_user_query, username, background_image,
                   status or '', intro_text or '', user_id)

        return redirect("/user/profile")
    # For GET Methods
    else:
        errors_dict = fillErrorDictionary(errors, errors_dict)
        return render_template("user/profile.html", errors=errors_dict, user=user[0], default_bg_images=default_bg_images)


@app.route("/user/profile/image", methods=['POST'])
@auth_required
def upload_user_profile_image():
    if 'file' not in request.files:
        return jsonify(
            isSuccess=False,
            message="File is not access"
        )

    file = request.files["file"]
    if file.filename == "":
        return jsonify(
            isSuccess=False,
            message="No Image Selected for uploading"
        )

    if file and check_image_validator(file.filename):
        filename = secure_filename(file.filename)
        _filename, file_extension = os.path.splitext(filename)
        uuid_img_name = uuid_url64() + file_extension
        dir = os.path.join("public/img/profile/", uuid_img_name)
        file.save(dir)

        updated_user_query = "UPDATE users SET image_avatar = ? WHERE id = ?"
        db.execute(updated_user_query, "/img/profile/" +
                   uuid_img_name, session["user_id"])

        return jsonify(
            isSuccess=True,
            message="File Upload Complete"
        )
    else:
        return jsonify(
            isSuccess=False,
            message="Not Allow Image Type"
        )


@app.route("/user/recipe/<recipe_id>/delete", methods=["POST"])
@auth_required
def user_recipe_delete(recipe_id):
    user_id = session["user_id"]
    recipe_query = "SELECT recipes.id, recipes.title, recipes.ingredients, recipes.youtube_link, recipes.steps, categories.id as category_id, categories.title as category_title FROM recipes "
    recipe_query += " INNER JOIN categories on categories.id = recipes.category_id "
    recipe_query += " WHERE recipes.user_id = ? and recipes.id = ?"

    recipe_exec = db.execute(recipe_query, user_id, recipe_id)
    recipe = recipe_exec[0] if len(recipe_exec) > 0 else None

    if recipe is None:
        return redirect("/user/recipe")
    else:
        recipe_del_query = "DELETE FROM recipes WHERE id = ? AND user_id = ?"
        recipe_del = db.execute(recipe_del_query, recipe_id, user_id)

        flash("Successfully Deleted!")

        return redirect("/user/recipe")


@app.route("/user/recipe/<recipe_id>/edit",  methods=["GET", "POST"])
@auth_required
def user_recipe_edit_page(recipe_id):
    categories = get_all_food_categories()
    errors = []
    errors_dict = {
        'title': '',
        'ingredients': '',
        'steps': '',
        'category_id': '',
        'youtube_link': '',
    }

    old_request = {
        'title': '',
        'ingredients': '',
        'category_id': '',
        'steps': '',
        'youtube_link': '',
    }

    user_id = session["user_id"]

    recipe_query = "SELECT recipes.id, recipes.title, recipes.ingredients, recipes.youtube_link, recipes.steps, categories.id as category_id, categories.title as category_title FROM recipes "
    recipe_query += " INNER JOIN categories on categories.id = recipes.category_id "
    recipe_query += " WHERE recipes.user_id = ? and recipes.id = ?"

    recipe_exec = db.execute(recipe_query, user_id, recipe_id)
    recipe = recipe_exec[0] if len(recipe_exec) > 0 else None

    if request.method == "POST":
        title = request.form.get("title")
        ingredients = request.form.get("ingredients")
        steps = request.form.get("steps")
        youtube_link = request.form.get("youtube_link")
        category_id = request.form.get("category") or '1'

        fillOldRequest('title', title, old_request)
        fillOldRequest('ingredients', ingredients, old_request)
        fillOldRequest('category_id', category_id, old_request)
        fillOldRequest('steps', steps, old_request)
        fillOldRequest('youtube_link', youtube_link, old_request)

        # Ensure title was submitted
        if not title:
            errors.append(
                FormError("title", "Title is required", title))

        if not ingredients:
            errors.append(
                FormError("ingredients", "Ingredients are required", ingredients))

        if not steps:
            errors.append(
                FormError("steps", "Steps are required", steps))

        if len(errors) > 0:
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("user/recipe_edit.html", errors=errors_dict, categories=categories, recipe=recipe)

        try:
            query = "UPDATE recipes SET title = ?, ingredients = ?, steps = ?, category_id = ?, youtube_link = ? WHERE id = ? AND user_id = ?"
            update_recipe = db.execute(
                query, title, ingredients, steps, category_id, youtube_link or "", recipe["id"], user_id)

            # Flash Messaging
            flash("Succesfully Updated Recipe!")

            # Redirect new Recipe List
            return redirect("/user/recipe")
        except:
            errors.append(FormError("image", "Image file is not valid", ''))
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("user/recipe_edit.html", recipe=recipe, errors=errors_dict, categories=categories)
    else:
        errors_dict = fillErrorDictionary(errors, errors_dict)
        return render_template("user/recipe_edit.html", recipe=recipe, errors=errors_dict, categories=categories)


@app.route("/user/recipe/<recipe_id>",  methods=["GET"])
@auth_required
def user_recipe_detail_page(recipe_id):

    user_id = session["user_id"]
    recipe_query = "SELECT recipes.id, recipes.image, recipes.title, recipes.ingredients, recipes.youtube_link, recipes.steps, "
    recipe_query += " categories.id as category_id, categories.title as category_title, "
    recipe_query += " users.id as user_id, users.image_avatar as user_image_avatar, users.name as user_name "
    recipe_query += " FROM recipes INNER JOIN categories on categories.id = recipes.category_id "
    recipe_query += " INNER JOIN users on users.id = recipes.user_id "
    recipe_query += " WHERE recipes.user_id = ? and recipes.id = ?"
    recipe_exec = db.execute(recipe_query, user_id, recipe_id)
    recipe = recipe_exec[0] if len(recipe_exec) > 0 else None
    
    if not recipe is None:
        recipe["ingredients"] = json.loads(recipe["ingredients"]) 
        recipe["steps"] = json.loads(recipe["steps"]) 

    return render_template("user/recipe_detail.html", recipe=recipe)


@app.route("/user/recipe",  methods=["GET"])
@auth_required
def user_recipe_page():
    # Total Per Page
    items_per_page = 10

    # For Page Query
    page = request.args.get('page')
    page = int(page) if (page and int(page) > 0) else 1
    offset = 0 if page == 1 else (page - 1) * items_per_page + 1

    # Total Recipe Count related User
    user_id = session["user_id"]
    total_query = "SELECT COUNT(id) as total_row FROM recipes WHERE user_id = ?"
    total_execute = db.execute(total_query, user_id)
    total_rows = total_execute[0]

    # Retrieving Paginate Recipies
    paginage_query = "SELECT id, title, image, category_id, user_id FROM recipes WHERE user_id = ? LIMIT 10 OFFSET " + \
        str(offset)
    recipes = db.execute(paginage_query, user_id)

    # Total Page
    total_page = math.ceil(total_rows['total_row'] / items_per_page)

    return render_template("user/recipe.html", recipes=recipes, page=page, total_page=total_page)


@app.route("/user/recipe/create",  methods=["GET", "POST"])
@auth_required
def user_recipe_create_page():
    categories = get_all_food_categories()
    errors = []
    errors_dict = {
        'title': '',
        'image': '',
        'ingredients': '',
        'steps': '',
        'category_id': '',
        'youtube_link': '',
    }

    old_request = {
        'title': '',
        'ingredients': '',
        'category_id': '',
        'steps': '',
        'youtube_link': '',
    }

    if request.method == "POST":
        title = request.form.get("title")
        ingredients = request.form.get("ingredients")
        steps = request.form.get("steps")
        youtube_link = request.form.get("youtube_link")
        category_id = request.form.get("category") or '1'

        fillOldRequest('title', title, old_request)
        fillOldRequest('ingredients', ingredients, old_request)
        fillOldRequest('category_id', category_id, old_request)
        fillOldRequest('steps', steps, old_request)
        fillOldRequest('youtube_link', youtube_link, old_request)

        # Ensure title was submitted
        if not title:
            errors.append(
                FormError("title", "Title is required", title))

        if not ingredients:
            errors.append(
                FormError("ingredients", "Ingredients are required", ingredients))

        if not steps:
            errors.append(
                FormError("steps", "Steps are required", steps))

        if 'image' not in request.files:
            errors.append(
                FormError("image", "Image file is required", ''))

        if not check_image_file_valid(request.files['image']):
            errors.append(
                FormError("image", "Image file is not valid", ''))

        if len(errors) > 0:
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("user/recipe_create.html", errors=errors_dict, categories=categories, old_request=old_request)

        # After All Validation End
        file = request.files["image"]
        filename = secure_filename(file.filename)
        _filename, file_extension = os.path.splitext(filename)
        uuid_img_name = uuid_url64() + file_extension
        dir = os.path.join("public/img/recipe/", uuid_img_name)
        file.save(dir)

        try:
            query = "INSERT INTO recipes (title, ingredients, steps, user_id, category_id, image, youtube_link) VALUES (?, ?, ?, ?, ?, ?, ?)"
            new_recipe = db.execute(query, title, ingredients, steps,
                                    session["user_id"], category_id, "/img/recipe/" + uuid_img_name, youtube_link or "")

            # Flash Messaging
            flash("Succesfully Created Recipe!")

            # Redirect new Recipe List
            return redirect("/user/recipe")
        except:
            errors.append(FormError("image", "Image file is not valid", ''))
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("user/recipe_create.html", errors=errors_dict, categories=categories, old_request=old_request)
    else:
        return render_template("user/recipe_create.html", categories=categories, errors=errors_dict, old_request=old_request)
