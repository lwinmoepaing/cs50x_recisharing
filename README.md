# ReciSharing

## CS50
>This is my final project for the CS50x2022 Introduction to Computer Sciense.
>Computer Science, Python, Flask Web Framework, HTML, CSS, JAVASCRIPT, CS50

#### Video Demo : 

#### Idea :
- The main idea of the project is recipe-sharing platform where user can share their own recipes and for Food enthusiasts who's looking for favorite recipe. They can find easily and share their own.

#### Database Structure :
All information about users, recipes data are stored in ```database.db``` .There are 3 tables, Users for Authenticate, Recipes For User's Recipe Data, And Category is relation with Recipes Table.

- First, table 'users' Where I put, id (primary key), name (unique for not repeated account), password (hasing), image_avatar (profile_picture), background_image (for their page background wallpaper), status (for version2 not for current), intro_text (for v2), role_id (integer 1 is for 'admin', 2 is 'normal_user' , but v1 is only allowed 2 for 'normal_user'), create_at(timestamp) 

- Second table is 'categories' for realation with Recipe's Category. There are id (primary key), title, icon_name (for v2), is_block (for version 2, is 0 mean 'enable', if 1 this category is 'disabled'), create_at(timestamp), updated_at(timestamp) 

- Third Table is for recipes data. This table is , called 'recipes', id (primary key), title, ingredients, steps (for instruction list), image (for recipe image), youtube_link (for embeded link), category_id (Foreign key for id of 'categories' table), user_id (Foreign key for id of 'users' table),

#### Features :

Login User
- Login User can CRUD for their recipes.
- Login User can CRUD for their profile.
- Login User can visit Recipe Owner Profile.
- Login User can search Recipe by Category , Title or Both.

Guest User
- Guest User can search Recipe by Category , Title or Both.\
- Guest User can also visit Recipe Owner Profile.

#### Demo Screencast :

![DemoScreen gif](./demo.gif)


#### Tricky Part for Me!!


#### All requirement installtaions for project
It's inside ```requirements.txt``` 

#### How to Install All Modules
``` pip install -r requirements.txt ```

### Modules Which I used in this project
> Flask

> Flask-Session

> CS50

### Folder Structure
```
.
├── app
│   │
│   ├── lib
│   │   └──     # All Helper Functions 
│   │
│   ├── middleware
│   │   └──     # All Middleware 
│   │
│   ├── routes
│   │   └──     # All Routes python files
│   │
│   └── __init__.py # Config All Flask App
│ 
│    
├── public      # All Static Files
│   │
│   ├── css     # All Css 
│   │
│   ├── img     # All Images
│   │
│   └── js      # All Javscripts
│  
├── app.py
├── database.db     # Database File
├── requirements.txt # All modules dependencies
└── README.md
```

## About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.

- Where I get CS50 course?
https://cs50.harvard.edu/x/2022