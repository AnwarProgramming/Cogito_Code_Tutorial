from flask import Flask

from flask_sqlalchemy import SQLAlchemy 

from flask_security import UserMixin, RoleMixin, Security, SQLAlchemyUserDatastore



db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)

    fs_uniquifier = db.Column(db.String(255), unique = True, nullable = False) 
    fs_token_uniquifier = db.Column(db.String(255), unique = True, nullable = False)

    roles = db.relationship('Role', secondary = 'user_role', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique = True, nullable = False)
    description = db.Column(db.String(150), nullable = True)

    def __repr__(self):
        return f'<Role {self.name}>'

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key = True)
    
    def __repr__(self):
        return f'<UserRole user_id={self.user_id} role_id={self.role_id}>'



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_name.db'
app.config['SECURITY_PASSWORD_SALT'] = 'my_passkey_is_salty'
app.config['SECRET_KEY'] = 'the_key_is_secret'

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db,User,Role)
security = Security(app,user_datastore)



if __name__ == '__main__':
    app.run(debug=True)










# from flask import Flask, request, jsonify

# # pip install flask_sqlalchemy
# from flask_sqlalchemy import SQLAlchemy 

# # pip install flask_security_too
# from flask_security import UserMixin, RoleMixin, Security, SQLAlchemyUserDatastore

# # 1.SQLAlchemyUserDatastore (The Bridge):
# # This class is the "manager" for your user and role data. It acts as an abstraction layer between Flask-Security and your actual database.
# # Its Job: It handles the low-level database operations (Create, Read, Update, Delete).
# # so you don't have to write manual SQL or SQLAlchemy queries for user management.
# # Key Functions:
# #   create_user(): Handles password hashing and saving a new user.
# #   add_role_to_user(): Manages the many-to-many link you defined earlier.
# #   find_user(): Quickly fetches a user by email or ID.

# # 2. Security (The Engine):
# # This is the main extension class that initializes Flask-Security. It plugs the "Bridge" (the datastore) into your Flask application.
# # Its Job: It sets up the actual web features, such as login/logout routes, register pages, and forgot-password emails.

# db = SQLAlchemy() #creating an instance(object) 'db' of the 'SQLAlchemy' class.

# # The db object becomes the main database handler for your Flask app. It provides:
# # 1.Database connection handling
# # 2.ORM features
# # 3.Table/model definitions
# # 4.Query support
# # 5.Session management

# # You later use it like this:
#         # class User(db.Model):
#         #     id = db.Column(db.Integer, primary_key=True)
#         #     name = db.Column(db.String(100))
# # Here:
# # db.Model → db.Model is not a table itself; it is the base class that your own Python classes inherit from to define a database table;
# # db.Column → defines a table column
# # db.Integer → integer datatype
# # db.String → string datatype

# ### So db acts like a toolbox containing all database-related functionality.

# # An 'instance' is an object created from a particular class.

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(150), unique = True, nullable = False)
#     password = db.Column(db.String(150), nullable = False)
#     email = db.Column(db.String(150), unique = True, nullable = False)

#     #Additional fields for Flask-Security
#     fs_uniquifier = db.Column(db.String(255), unique = True, nullable = False) 
#     fs_token_uniquifier = db.Column(db.String(255), unique = True, nullable = False)
#     # fs_uniquifier:A permanent unique ID marker for the user (random string).
#     # fs_token_uniquifier: A global token version key used to invalidate ALL sessions/tokens.

#     roles = db.relationship('Role', secondary = 'user_role', backref=db.backref('users', lazy='dynamic'))

#     def __repr__(self):
#         return f'<User {self.username}>'
# # UserMixin is a helper class from Flask-Security / Flask-Login that adds authentication-related features to your User model.
# ## It automatically provides methods like:
# # is_authenticated
# # is_active
# # is_anonymous
# # get_id()
# ## These help Flask manage:
# # login sessions
# # authentication
# # user identification

# class Role(db.Model,RoleMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), unique = True, nullable = False)
#     description = db.Column(db.String(150), nullable = True)

#     def __repr__(self):
#         return f'<Role {self.name}>'


# # RoleMixin adds role/permission-related functionality to your Role model.
# # Used for roles like:
# # Admin
# # Editor
# # Viewer

# class UserRole(db.Model): # many-many relation
#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
#     role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key = True)
#     # primary_Key on both user_id and role_id creates a composite primary key which means (user_id, role_id) together must be unique.

#     def __repr__(self):
#         return f'<UserRole user_id={self.user_id} role_id={self.role_id}>'



# app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_name.db'
# app.config['SECURITY_PASSWORD_SALT'] = 'my_passkey_is_salty'
# app.config['SECRET_KEY'] = 'the_key_is_secret'

# # SECRET_KEY is used by Flask for securely signing session cookies and CSRF tokens.
# # SECRET_KEY is the main cryptographic key used by Flask to protect sensitive data.
# # Flask uses it for:
#     # Session cookies
#     # CSRF protection
#     # Secure token signing
#     # Remember-me login cookies
#     # Flash messages

# ### Visual workflow of(SECRET_KEY)
# # User Login
# #     ↓
# # Flask Creates Session
# #     ↓
# # Session Signed with SECRET_KEY
# #     ↓
# # Cookie Sent to Browser
# #     ↓
# # Browser Sends Cookie Back
# #     ↓
# # Flask Verifies Signature
# #     ↓
# # Valid → Allow Access
# # Invalid → Reject


# ### SECURITY_PASSWORD_SALT
# # This is an additional security value called a salt.
# # A salt adds randomness to cryptographic operations.
# # SECURITY_PASSWORD_SALT is commonly used by extensions like Flask-Security for password hashing/token generation.

# ### relationship between both
# # SECRET_KEY
# #     +
# # SECURITY_PASSWORD_SALT
# #     ↓
# # Secure Tokens

# db.init_app(app) #This line connects your database object (db) to your Flask application (app).
# # first configure the app and then initialize

# user_datastore = SQLAlchemyUserDatastore(db,User,Role)
# security = Security(app,user_datastore)


# ##### Big-picture architecture
# # Browser
# #    |
# # HTTP Request
# #    |
# # Flask App
# #    |
# # Flask-Security
# #    |
# # SQLAlchemyUserDatastore
# #    |
# # SQLAlchemy ORM
# #    |
# # Database
# #########

# if __name__ == '__main__':
#     app.run(debug=True)