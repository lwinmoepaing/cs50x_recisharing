--  Creating Categories Table
CREATE TABLE "categories" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"icon_name"	TEXT NOT NULL DEFAULT '/img/category/cat_icon_1.png',
	"is_block"	INTEGER NOT NULL DEFAULT 0,
	"created_at"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- Creating Users Table
CREATE TABLE "users" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"image_avatar"	TEXT NOT NULL DEFAULT '/img/profile/default.png',
	"background_image"	TEXT NOT NULL DEFAULT '/img/background/default_1.jpg',
	"status"	TEXT,
	"intro_text"	TEXT,
	"role_id"	INTEGER NOT NULL DEFAULT 2,
	"created_at"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("name")
);

-- Creating Recipes Table
CREATE TABLE "recipes" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"ingredients"	TEXT NOT NULL DEFAULT '[]',
	"steps"	TEXT DEFAULT '[]',
	"user_id"	INTEGER,
	"category_id"	INTEGER,
	"image"	TEXT NOT NULL DEFAULT '/img/recipe/default.jpg',
	"youtube_link" TEXT DEFAULT '',
	FOREIGN KEY("category_id") REFERENCES "categories"("id") ON DELETE SET NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE SET NULL
);

-- Seeding Initial Categories State
INSERT INTO "categories" ("id", "title", "icon_name") VALUES (NULL,'Bakery & Cakes', '/img/category/bevarage_and_cake.png');
INSERT INTO "categories" ("id", "title", "icon_name") VALUES (NULL,'Curry', '/img/category/curry.png');
INSERT INTO "categories" ("id", "title", "icon_name") VALUES (NULL,'Dessert', '/img/category/dessert.png');
INSERT INTO "categories" ("id", "title", "icon_name") VALUES (NULL,'Fast Food', '/img/category/fast_food.png');
INSERT INTO "categories" ("id", "title", "icon_name") VALUES (NULL,'Ice Cream', '/img/category/ice_cream.png');
INSERT INTO "categories" ("id", "title", "icon_name") VALUES (NULL,'Pizza', '/img/category/pizza.png');
INSERT INTO "categories" ("id", "title", "icon_name") VALUES (NULL,'Steak', '/img/category/steak.png');