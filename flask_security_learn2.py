from flask import Flask

from flask_sqlalchemy import SQLAlchemy 

from flask_security import UserMixin, RoleMixin, Security, SQLAlchemyUserDatastore



db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    active = db.Column(db.Boolean(), default = True)

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
    def __repr__(self):
        return f'<UserRole user_id={self.user_id} role_id={self.role_id}>'



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security.db'
app.config['SECURITY_PASSWORD_SALT'] = 'my_passkey_is_salty'
app.config['SECRET_KEY'] = 'the_key_is_secret'

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db,User,Role)
security = Security(app,user_datastore)

def create_database():
    with app.app_context():
        db.create_all()

        user_role = user_datastore.find_or_create_role(name='user', description='User Role: This role is valid for every user')
        admin_role = user_datastore.find_or_create_role(name='admin', description='Admin Role: This is the superuser of the application')
        manager_role = user_datastore.find_or_create_role(name='manager', description='Manager Role: This person is responsible for managing the store')

        if not user_datastore.find_user(username='super_user'):
            user_datastore.create_user(
                username='super_user',
                email='superuser@gmail.com',
                password='superuser',

                roles = [admin_role,manager_role]
                )


        if not user_datastore.find_user(username='manager'):
            user_datastore.create_user(
                username='manager',
                email = 'manager@gmail.com',
                password='manager',
                
                roles=[manager_role]
                )

        db.session.commit()
        print("Database created and initial data added successfully.")



if __name__ == '__main__':
    create_database()
    app.run(debug=True)