from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# Create an Instance of SQLAlchemy & save to variable db

db = SQLAlchemy()
bcrypt = Bcrypt()
def connect_db(app):
    db.app = app
    db.init_app(app)






# User Model -------------------------------------------------------------------------------

class User(db.Model):
    """ User Model Instance """

    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True, unique = True )
    username = db.Column( db.Text, nullable = False, unique = True )
    password = db.Column( db.Text, nullable = False )
    email = db.Column( db.Text, nullable = False, unique = True )
    dob = db.Column( db.Date, nullable = False )
    picture = db.Column( db.Text, nullable = True )
    # searches = db.Column( db.Integer, db.ForeignKey('searches.id'))
    # favorites = db.Column( db.Integer, db.ForeignKey('favorites.id'))

    # search = db.relationship( 'Search', backref = 'users' )
    # favorite = db.relationship( 'Favorite', backref = 'users' )



    def __init__( self, username, password, email, dob, picture ):
        """ Initalize the attributes of the User Class """

        self.username = username
        self.password = password
        self.email = email
        self.dob = dob
        self.picture = picture

    def __repr__(self):
        """ Representation Method of User Class """

        s = self 

        return f'User || id = {s.id} || username = {s.username} || password = {s.password} || email = {s.email} || dob = {s.dob} || picture_url = {s.picture} || searches = {s.searches}'
    
    def update_profile( self, username, email, dob, picture ):
        """ Update user profile information """

        self.username = username
        self.dob = dob
        self.email = email
        self.picture = picture

        return f'You have successfully updated your profile: {self.username} || {self.email} || {self.dob} || {self.picture}'

    @classmethod
    def create( cls, username, password, email, dob, picture ):
        """ Creates a new user """

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf-8')

        return cls( username = username, password = hashed_utf8, email = email, dob = dob, picture = picture )
    
    @classmethod
    def login( cls, username, password ):
        """ Login User """

        user = User.query.filter_by(username = username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


# Search Model ------------------------------------------------------------------------------ 

class Search(db.Model):
    """ Search Model Instance """

    __tablename__ = 'searches'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True, unique = True )
    search_term = db.Column( db.Text, nullable = True )
    search_timestamp = db.Column( db.Text, nullable = True )
    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ))

    users = db.relationship( 'User', backref = 'searches' )

    def __init__(self, search_term, search_timestamp, user_id ):
        """ Initalize the attributes of the Search class """

        self.search_term = search_term
        self.search_timestamp = search_timestamp
        self.user_id = user_id
        
    def __repr__(self):
        """ Representation Method of Search Class """

        s = self
        
        return f'Search || search_term = {s.search_term} || search_timestamp = {s.search_timestamp}'        

    @classmethod
    def add_search_to_history( cls, search_term, search_timestamp, user_id ):
        """ Adds term search to user search history """

        search = Search( search_term, search_timestamp, user_id )
        db.session.add( search )
        db.session.commit() 

        return search
    
    @classmethod
    def clear_search_history( cls, user_id ):
        """ Flushes all search history for user """

        searches = Search.query.filter_by( user_id = user_id ).all()
        
        db.session.delete( searches )
        db.session.commit()
        
        return searches

# Favorite Model -----------------------------------------------------------------------------

class Favorite(db.Model):
    """ Favorite Model Instance """

    __tablename__ = 'favorites'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True, unique = True )
    favorited_page = db.Column( db.Text, nullable = True )
    favorited_timestamp = db.Column( db.Time, nullable = True )
    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ))

    user = db.relationship( 'User', backref = 'favorites' )

    def __init__(self, favorited_page, favorited_timestamp, user_id ):
        """ Initalize the attributes of the Favorite class """

        self.favorited_page = favorited_page
        self.favorited_timestamp = favorited_timestamp
        self.user_id = user_id

    def __repr__(self):

        f = self

        return f'{f.favorited_page} {f.favorited_timestamp}'
    
    @classmethod
    def add_to_favorites(cls, favorited_page, favorited_timestamp, user_id ):
        """ Adds Page to favorited pages """

        favorite = Favorite( favorited_page, favorited_timestamp, user_id )
        db.session.add( favorite )
        db.session.commit()

        return favorite

