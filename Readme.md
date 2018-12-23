# Item Catalog
In this project, you will be developing a web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items.
You will be creating this project essentially from scratch, no templates have been provided for you. This means that you have free reign over the HTML, the CSS, and the files that include the application itself utilizing Flask.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
## Prerequisites
* To start on this project, you'll need database software (provided by a Linux virtual machine) , We're using tools called `Vagrant` and `VirtualBox` to install and manage the VM.
* You'll be doing these exercises using a Unix-style terminal on your computer. If you are using a **Mac**  or **Linux** system, your regular terminal program will do just fine. On **Windows**, we recommend using the **Git Bash** terminal that comes with the Git software.
* Download the **VM** configuration.
## Installing
* Vagrant: https://www.vagrantup.com/downloads.html
* Virtual Machine: https://www.virtualbox.org/wiki/Downloads
* Download a FSND virtual machine:https://github.com/udacity/fullstack-nanodegree-vm
   and probably you will find the file in your “Download” folder.
* we recommend using the **Git Bash** terminal that comes with the Git
  software. If you don't already have Git installed, download Git from git-scm.com.
## Tests and Running in Command Line
* Once you get the above software installed, follow the following instructions:
`vagrant --version`
#If Vagrant is successfully installed, you will be able to run vagrant --version
in your terminal to see the version number.
`cd vagrant`
`vagrant up`
`vagrant ssh`
`cd /vagrant`
`mkdir catalog`
#The Directory **catalog** we put inside all the files that we will work on.
`cd catalog` 
`touch application.py`  
#The file **application.py** will contain the Python code using Flask framework,(its name can be changed to any name you like).
`touch database_setup`
#The file **database_setup** is on the database configuration code.
`touch lotsofmenus`
#The file **lotsofmenus** We will put the database we use in this project.
`mkdir static`
#The Directory **static** We put CSS files into the design of the web application.
`mkdir templates`
#The Directory **templates** We create html pages for the web application.
- For this project, all the work will be on your Linux machine, so always make sure
you logged in by using the following commands: vagrant up, then vagrant ssh, 
then cd /vagrant.
Note: Files in the VM's /vagrant directory are shared with the vagrant folder on     your computer. But other data inside the VM is not.

## How will I complete this project?
This project is connected to the Full Stack Foundations and Authentication and Authorization courses, but depending on your background knowledge you may not need the entirety of both courses to complete this project. Here's what you should do:
* Install Vagrant and VirtualBox
* Clone the fullstack-nanodegree-vm
* Launch the Vagrant VM (vagrant up)
* Write your Flask application locally in the vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM).
* Run your application within the VM (python /vagrant/catalog/application.py)
* Access and test your application by visiting http://localhost:5000 locally
* Get started with this helpful [guide](https://docs.google.com/document/d/e/2PACX-1vT7XPf0O3oLCACjKEaRVc_Z-nNoG6_ssRoo_Mai5Ce6qFK_v7PpR1lxmudIOqzKo2asKOc89WC-qpfG/pub?embedded=true)
* You can find the link to the fullstack-nanodegree-vm [here](https://github.com/udacity/fullstack-nanodegree-vm)

## Python code quality
Your code should be written with good Python style. The [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) is an excellent standard to follow. You can do a quick check using the `pep8` command-line tool.
### Examples:
#### Example code Flask application 
```
#!/usr/bin/env python3

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Company, MenuCars
from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify
from flask import session as login_session
from flask import make_response
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Company Cars"


@app.context_processor
def inject_session_in_all_templates():
    return dict(login_session=login_session)


# Connect to Database and create database session
engine = create_engine('sqlite:///companymenu.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
```
#### Example database configuration code
```
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }
```
### Example of the database we will use
```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Company, MenuCars

engine = create_engine('sqlite:///companymenu.db')
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


# Menu for Company Toyota
company1 = Company(name="Toyota")
session.add(company1)
session.commit()

MenuCars1 = MenuCars(name="Yaris",
                     description="The Yaris is a sedan and wheel-drive type.",
                     price="45,900 SR", company=company1)
session.add(MenuCars1)
session.commit()

```
### Example the code of html pages
```
<html>
<head>
{% include "loginorlogout.html" %}
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='styles.css') }}">
</head>

<body>
<div class = 'pane'>
<h1>Menu Company</h1>
<a href="{{url_for('newCompany')}}" ><h4><input type='submit' value='Create a New Company'></h4></br>

<!--MESSAGE FLASHING EXAMPLE -->
{% with messages = get_flashed_messages() %}
{% if messages %}

<ul>
{% for message in messages %}
  <li><strong>{{message}}</strong></li>
  {% endfor %}
</ul>
{% endif %}
{% endwith %}


{% for company in companies %}

<a href = "{{url_for('menuCars', company_id = company.id)}}"><p><h1>{{company.name}}</h1></p></a>

<p><a href = "{{url_for('editCompany', company_id = company.id)}}">Edit</a></p>

<p> <a href = "{{url_for('deleteCompany', company_id = company.id)}}">Delete</a> </p></br>


{% endfor %}

</div>
</body>

</html>
```
### Example the code of file stayle.CSS
```
body            { font-family: sans-serif; background-color: #9e9e9e52; }
 h1, h2, h3, h4       { color: #819e60; }
h1, h2          { font-family: 'Georgia', serif; margin: 0; }
h1              { border-bottom: 1px solid #FFCA28; }
h2              { font-size: 1.2em; }

p               { color: #823d3d;}

a {text-decoration: none; color:#000000; font-size: .85em;}

.pane {position:absolute; left: 25%; border: 2px solid;
    border-radius: 25px; padding: 5px; margin: 5px; border-color: #3e3434; background-color: #a02f2f; }
.header         {left:50%; text-align: center;}
.name {width:50%;display: inline-block; float: left;}
.description {}
.price {text-align: right; width:50%; float: right; }
.editdeletepane{}

.flash          { background: #881b1b; }
```
### Project Display Example
[ http://localhost:5000](https://drive.google.com/open?id=1ue7O7Wjpn33GNIIrxsAca7IhzsfMTHAL)
Note: The screenshots on this page are just examples of one implementation of the minimal functionality. You are encouraged to redesign and strive for even better solutions.

## More Information
* [SQLAlchemy](https://docs.sqlalchemy.org/en/rel_0_9/orm/query.html)
* [Welcome to Flask](http://flask.pocoo.org/docs/1.0/)
* [Tools for Web Developers](https://developers.google.com/web/tools/chrome-devtools/?utm_source=dcc&utm_medium=redirect&utm_campaign=2018Q2)
* [Getting started with HTML](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started)
* [Intro to HTML and CSS](https://classroom.udacity.com/courses/ud197/lessons/3483858580/concepts/35153985360923https://classroom.udacity.com/courses/ud001/lessons/6987421963/concepts/74229205890923)
* [JSON](https://en.wikipedia.org/wiki/JSON)
* [Create an OAuth Server](https://lepture.com/en/2013/create-oauth-server)
* [Session hijacking](https://en.wikipedia.org/wiki/Session_hijacking)
* [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
* [console developers](https://console.developers.google.com/apis/dashboard?project=companycars-225023)
* [PEP8](https://pypi.org/project/pep8/)
## Author
* **abdulrahman ali alfaifi**
## Acknowledgments
* Hat tip to anyone whose code was used
* Inspiration
* etc











  