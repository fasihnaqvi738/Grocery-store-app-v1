# Grocery Store App

## Introduction

The Grocery Store App is an application that allows users to browse and purchase groceries online.
It is a multiuser app that has one admin and many users


## Features
- The admin can add/update/delete products 
- The users can register themselves and login to their dashboard
- The users can browse and search for products by category or name.
- The users can view products , add them to cart and purchase them
- The users can view their profile
- The cart itself decreases the quantity of a product added if its stock is reduced by admin or was reduced due to purchase by some other   user (basically can’t exceed the stock)

- The admin has a fixed username and password(and no option to register as an admin):
    username: admin123
    password: adminpass
    
## Installation

- You need to install flask in your system-

    In terminal type:
        pip install flask

- You need to install flask-sqlalchemy in your system-
    In terminal type: 
        pip install flask-sqlalchemy
       
- To view the database :
    Go to https://sqlitebrowser.org/dl/ and download the latest version of DB Browser, install it and open the database.db file from your system.To view the data click 'browse data' (click refresh button after every activity that tends to update the database)

##  Usage
SECRET_KEY='secret-key'


-  Download the project folder and unzip it to your preferred location.

- Open the project folder  in your preferred code editor. You should see the project's files and folders within the editor.

- After installing the required libraries run the 'app.py' file and go to the url where it is running, the application should start with homepage
