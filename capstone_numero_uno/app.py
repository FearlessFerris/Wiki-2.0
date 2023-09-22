from flask import Flask, request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests, json, datetime

from models import db, connect_db, User, Search, Favorite
from forms import CreateUserForm, LoginUserForm, SearchPagesForm, EditUserFrom, AddFavoritePage

from api import SEARCH_PAGE_BASE, GET_PAGE_BASE



app = Flask(__name__)
t = datetime.datetime.today()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wikipedia'
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'imasecretkeyshh'
debug = DebugToolbarExtension(app)
app.app_context().push()
connect_db(app)





@app.route('/')
def homepage():
    """ Routes to Application Homepage """

    form = SearchPagesForm()

    return render_template('homepage.html', form = form )

# Create User / Login / Profile -------------------------------------------------

@app.route('/create-user', methods = ['GET', 'POST'])
def create_user_form():
    """ Routes to display form and handle form submission """
    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        dob = form.dob.data
        picture = form.picture.data
        new_user = User.create( username, password, email, dob, picture )
        flash( f'You have successfully created user { new_user.username }')
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    
    else:
        return render_template('create-user-form.html', form = form)



@app.route('/login', methods = ['GET', 'POST'])
def user_login():
    """ Routes to login User """

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.login(username, password)

        if user:
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Incorrect Name or Password']
        
    return render_template('login.html', form = form )



@app.route('/logout')
def logout_user():
    """ Routes to logout user """

    session.pop('user_id')
    return redirect('/')



@app.route('/user-profile')
def show_profile():
    """ Routes to user profile page """

    user = User.query.get(session['user_id'])

    return render_template('user-profile.html', user = user )



@app.route('/edit-profile', methods = ['GET', 'POST'])
def edit_profile():
    """ Routes to edit profile information """

    form = EditUserFrom()
    user_id = session.get('user_id')

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        dob = form.dob.data
        picture = form.picture.data
        user = User.query.get_or_404( user_id )
        user.update_profile( username, email, dob, picture )
        flash(f'You have successfully updated your profile!')
        db.session.commit()
        
        return redirect('/')
    
    else:
        return render_template('edit-user.html', form = form )



# Search Pages -----------------------------------------------------------------

@app.route('/search-pages', methods = ['GET', 'POST'])
def search_pages():
    """ Routes to search pages based on form input """

    form = SearchPagesForm()
    
    if form.validate_on_submit():
        search_term = form.search_term.data
        url = SEARCH_PAGE_BASE
        response = requests.get( url, params = { 'q' : search_term })
        data = response.json()
        pages = data['pages']
        print( data )

        time = t
        user = session.get('user_id')
        search = Search.add_search_to_history( search_term, time, user )
        
        return render_template('search-pages.html', form = form, data = data, pages = pages )

    else:
        return redirect('/search-pages')
    


@app.route('/get-page')
def show_page_info():
    """ Routes to display selected page information """

    form = AddFavoritePage()

    page = request.args.get('title')
    url = f'{GET_PAGE_BASE}{page}'
    response = requests.get( url )
    data = response.json()
    favorited_page = data['title']
    
    html_url = f'{GET_PAGE_BASE}{page}/html'
    html_response = requests.get( html_url )
    html = html_response.text
    
    # return html
    return render_template('page.html', data = data, html = html, favorited_page = favorited_page, form = form )



@app.route('/search-history', methods = ['GET', 'POST'])
def show_history():
    """ Routes to show users search history """ 

    if session.get('user_id'):
        searches = Search.query.order_by(Search.id.desc()).filter_by(user_id = session['user_id'])
    
    else:
        searches = Search.query.order_by(Search.id.desc()).filter_by(user_id = None)
    
    return render_template('search-history.html', searches = searches )



@app.route('/clear-history', methods = ['GET', 'POST'])
def clear_user_search_history():
    """ Routes to clear users search history """

    user = User.query.get_or_404( session['user_id'] )
    searches = Search.clear_search_history( user.id )

    return render_template('search-history.html', searches = searches )

# Favorites -------------------------------------------------------------------------------
    
@app.route('/favorites', methods = ['GET', 'POST'])
def add_show_favorites():
    """ Routes to add and show user favorited pages """

    user = User.query.get_or_404( session['user_id'] )
    user_id = user.id 
    form = AddFavoritePage()

    if form.validate_on_submit():
        favorited_page = request.args.get('favorited_page')
        favorited_timestamp = t
        favorite = Favorite.add_to_favorites( favorited_page, favorited_timestamp, user_id )

        return redirect('/favorites')

    else:
        favorites = Favorite.query.order_by(Favorite.id.desc()).filter_by(user_id = session['user_id'])
    
        return render_template('favorites.html', user = user, favorites = favorites, form = form )

   



