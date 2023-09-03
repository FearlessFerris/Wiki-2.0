from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests, json
from Secrets import SEARCH_PAGE_BASE, GET_PAGE_BASE
from forms import SignupNewUserForm, LoginUserForm, SearchPageForm




app = Flask(__name__)
app.config['SECRET_KEY'] = 'imasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)










# Page Search ----------------------------------------------------------

@app.route('/')
def homepage():
    """ Routes to application homepage """

    form = SearchPageForm()

    return render_template('homepage.html', form = form)



@app.route('/search-pages', methods = ['GET', 'POST'])
def search_pages():
    """ Routes to search pages based on search input """

    form = SearchPageForm()

    if form.validate_on_submit():
        search = form.search.data
        url = SEARCH_PAGE_BASE
        response = requests.get( url, params = { 'q' : search })
        data = response.json()
        pages = data['pages']
        print( data )
    
        return render_template('search-display.html', form = form, data = data, pages = pages )
    


@app.route('/get-page')
def show_page_info():
    """ Routes to display selected page information """

    page = request.args.get('title')
    url = f'{GET_PAGE_BASE}{page}/bare'
    response = requests.get( url )
    data = response.json()
    

    html_url = f'{GET_PAGE_BASE}{page}/html'
    html_response = requests.get( html_url )
    html = html_response.text
    

    print( html )

    return html
    return render_template('page.html', data = data, html = html )



# Login / Signup ----------------------------------------------------------

@app.route('/login', methods = ['GET', 'POST'])
def login_user():
    """ Routes to user login page """

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        flash(f'Welcome back {username}')
        return redirect('/')

    else:
        return render_template('login.html', form = form )



@app.route('/signup', methods = ['GET', 'POST'])
def signup_user():
    """ Routes to signup a new user """

    form = SignupNewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        flash(f'{username}, your account has been created!')
        return redirect('/login')
    
    else:
        return render_template('signup.html', form = form )



