#!/usr/bin/env python

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Company, MenuCars, User
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
engine = create_engine('sqlite:///companymenuwithusers.db')
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


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''Validate state token'''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    '''Obtain authorization code, now compatible with Python3'''
    code = request.data

    try:
        ''' Upgrade the authorization code into a credentials object'''
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    '''Check that the access token is valid.'''
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token
        )
    '''Submit request, parse response - Python3 compatible'''
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    '''If there was an error in the access token info, abort.'''
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Verify that the access token is used for the intended user.'''
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Verify that the access token is valid for this app.'''
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200
                                 )
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Store the access token in the session for later use.'''
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    '''Get user info'''
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    '''see if user exists, if it doesn't make a new one'''
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;\
        border-radius: 150px;-webkit-border-radius: 150px;\
        -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    '''Only disconnect a connected user.'''
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        '''Reset the user's sesson.'''
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("user logout")
        return response

    else:
        '''For whatever reason, the given token was invalid.'''
        response = make_response(json.dumps('Failed revoke token user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view  Company Information
@app.route('/company/JSON')
def menuCompanyJSON():
    company = session.query(Company).all()
    return jsonify(Company=[i.serialize for i in company])


@app.route('/company/<int:company_id>/menu/JSON')
def companyMenuJSON(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    menucars = session.query(MenuCars).filter_by(company_id=company_id).all()
    return jsonify(MenuCars=[i.serialize for i in menucars])


@app.route('/company/<int:company_id>/menu/<int:menu_id>/JSON')
def menuCarsJSON(company_id, menu_id):
    menucars = session.query(MenuCars).filter_by(id=menu_id).one()
    return jsonify(MenuCars=menucars.serialize)


# Show all company
@app.route('/')
@app.route('/company/')
def menuCompany():
    companies = session.query(Company).order_by(asc(Company.name))
    if 'username' not in login_session:
        return render_template('publicCompany.html', companies=companies)
    else:
        return render_template('menuCompany.html', companies=companies)


# Create a new Company
@app.route('/company/new/', methods=['GET', 'POST'])
def newCompany():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newcompany = Company(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newcompany)
        flash("new Company %s Successfully created!" % newcompany.name)
        session.commit()
        return redirect(url_for('menuCompany'))
    else:
        return render_template('newCompany.html')


# Edit a Company
@app.route('/company/<int:company_id>/edit/', methods=['GET', 'POST'])
def editCompany(company_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCompany = session.query(
        Company).filter_by(id=company_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCompany.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You\
         are not authorized to edit this company.\
          Please create your own company in order\
           to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedCompany.name = request.form['name']
        flash("Company Successfully Edited %s" % editedCompany.name)
        return redirect(url_for('menuCompany'))
    else:
        return render_template('editCompany.html', company=editedCompany)


# Delete a Company
@app.route('/company/<int:company_id>/delete/', methods=['GET', 'POST'])
def deleteCompany(company_id):
    CompanyToDelete = session.query(Company).filter_by(id=company_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if CompanyToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You\
         are not authorized to delete this company.\
          Please create your own company in order\
           to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(CompanyToDelete)
        flash("%s Successfully Deleted" % CompanyToDelete.name)
        session.commit()
        return redirect(url_for('menuCompany', company_id=company_id))
    else:
        return render_template('deleteCompany.html', company=CompanyToDelete)


# Show menu Cars
@app.route('/company/<int:company_id>/')
@app.route('/company/<int:company_id>/menu/')
def menuCars(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    creator = getUserInfo(company.user_id)
    carItems = session.query(MenuCars).filter_by(company_id=company_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template(
                'publicCars.html', carItems=carItems,
                company=company, creator=creator)
    else:
        return render_template(
                'menuCars.html', company=company,
                carItems=carItems, creator=creator)


# Create a new Car
@app.route('/company/<int:company_id>/new/', methods=['GET', 'POST'])
def addNewCar(company_id):
    if 'username' not in login_session:
        return redirect('/login')
    company = session.query(Company).filter_by(id=company_id).one()
    if login_session['user_id'] != company.user_id:
        return "<script>function myFunction() {alert('You\
         are not authorized to add new car to this company.\
          Please create your own company in order\
            to add.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newCars = MenuCars(
         name=request.form['name'],
         description=request.form['description'],
         price=request.form['price'],
         company_id=company_id, user_id=company.user_id)
        session.add(newCars)
        session.commit()
        flash('New information Cars %s Successfully Created.' % (newCars.name))
        return redirect(url_for('menuCars', company_id=company_id))
    else:
        return render_template('addNewCar.html',  company_id=company_id)


# Edit information Car
@app.route('/company/<int:company_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editInforamtionCar(company_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedInformation = session.query(MenuCars).filter_by(id=menu_id).one()
    company = session.query(Company).filter_by(id=company_id).one()
    if login_session['user_id'] != company.user_id:
        return "<script>function myFunction() {alert('You\
         are not authorized to edit information the Car to this company.\
          Please create your own company in order\
           to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedInformation.name = request.form['name']
        if request.form['description']:
            editedInformation.description = request.form['description']
        if request.form['price']:
            editedInformation.price = request.form['price']
        session.add(editedInformation)
        session.commit()
        flash("Information %s Successfully Edited." % (editedInformation.name))
        return redirect(url_for('menuCars', company_id=company_id))
    else:
        return render_template('editInforamtionCar.html',
                               company_id=company_id, menu_id=menu_id,
                               item=editedInformation)


# Delete a Car
@app.route(
            '/company/<int:company_id>/<int:menu_id>/delete/',
            methods=['GET', 'POST']
           )
def deleteInforamtionCar(company_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    company = session.query(Company).filter_by(id=company_id).one()
    itemToDelete = session.query(MenuCars).filter_by(id=menu_id).one()
    if login_session['user_id'] != company.user_id:
        return "<script>function myFunction() {alert('You\
         are not authorized to delete car to this company.\
          Please create your own company in order\
           to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Car %s Successfully Deleted." % (itemToDelete.name))
        return redirect(url_for('menuCars', company_id=company_id))
    else:
        return render_template('deleteInforamtionCar.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
