""" Seed file / Sample Data for Wiki 2.0 Application """

from models import User, Search, Favorite, db
from app import app



# Creating Tables 
# db.drop_all()
# db.create_all

u1 = User( username = 'James_Bond', password = 'bondjamesbond', email = 'james@gmail.com', dob = '10-01-1990', picture = '' )
u2 = User( username = 'BillyTheKid', password = 'bill', email = 'bill@gmail.com', dob = '09-02-1964', picture = '' )
u3 = User( username = 'Jim', password = 'jim', email = 'jim@gmail.com', dob = '06-19-2003', picture = '' )

s1 = Search( search_term = 'people', search_timestamp = '10/10/10 10:00', user_id = 1 )
s2 = Search( search_term = 'are', search_timestamp = '10/10/10 10:10', user_id = 2 )
s3 = Search( search_term = 'strange', search_timestamp = '10/10/10 10:00', user_id = 3 )



db.session.add( u1 )
db.session.add( u2 )
db.session.add( u3 )
db.session.commit()


db.session.add( s1 )
db.session.add( s2 )
db.session.add( s3 )
db.session.commit()

