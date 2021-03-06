from app import db, login
from flask_login import UserMixin #only for the user model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.String)

    def __repr__(self): #should return a unique identifying string
        return f'<User: {self.email} | {self.id}>'

    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']
        print(self.icon)

    def save(self):
        db.session.add(self) #add user to db session
        db.session.commit() #saves everything to db

    def get_icon_url(self):
        return f'https://ui-avatars.com/api/?name={self.icon.split()[0]}+{self.icon.split()[1]}&background=F3BB04&color=fff.svg'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
