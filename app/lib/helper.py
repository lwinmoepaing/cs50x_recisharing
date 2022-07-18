from app import db
import re
import uuid
import base64


def uuid_url64():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


class FormError(object):
    def __init__(self, formField, message, value):
        self.formField = formField
        self.message = message
        self.value = value


def fillErrorDictionary(errors, modified_dict):
    for error in errors:
        modified_dict[error.formField] = error.message
    return modified_dict


def fillOldRequest(key, value, modified_dict):
    modified_dict[key] = value or ''
    return modified_dict


def check_image_validator(filename):
    ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_all_food_categories():
    recipes_query = "SELECT id, title, icon_name, is_block FROM categories "
    recipes = db.execute(recipes_query)
    return recipes


def check_image_file_valid(file):
    if not file:
        return False
    if file.filename == "":
        return False
    if check_image_validator(file.filename):
        return True
    else:
        return False
