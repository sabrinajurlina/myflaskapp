from flask import render_template
from app import db, login
from flask_login import UserMixin #only for the user model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class PokemonUser(db.Model):
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    ability = db.Column(db.String)
    sprite = db.Column(db.String)

    def from_dict(self, data):
        self.name = data['name']
        self.base_experience = data['base_experience']
        self.hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.ability = data['ability']
        self.sprite = data['sprite']

    def save(self):
        db.session.add(self) #add pokemon to db session
        db.session.commit() #saves everything to db

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.String)
    team = db.relationship(Pokemon,
                secondary='pokemon_user',
                backref='users',
                lazy='dynamic'
                )
    wins = db.Column(db.Integer, default = 0)
    losses = db.Column(db.Integer, default = 0)

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

    def save(self):
        db.session.add(self) #add user to db session
        db.session.commit() #saves everything to db

    def get_icon_url(self):
        return f'https://ui-avatars.com/api/?name={self.icon.split()[0]}+{self.icon.split()[1]}&background=F3BB04&color=fff.svg'

    def check_team(self, pokemon_to_check):            
        if self.team.count()>0:
            return self.team.filter(Pokemon.poke_id == pokemon_to_check.poke_id).count()>0
            #where do we return the error if the pokemon is already caught?

    #add pokemon to our team if not already on our team
    def catch_poke(self, pokemon):
        print(self.team, 'TEAM')
        if not self.check_team(pokemon) and self.team.count()<5:
            self.team.append(pokemon)
            db.session.commit()

    def delete_poke(self, pokemon):
        if self.check_team(pokemon):
            self.team.delete(pokemon)
            db.session.commit()

    def show_team(self):
        team = self.team
        return team

    def show_players(self):
        players = User.query.filter(User.id != self.id).all()
        return players

    def battle(self, opponent_id):
        if self.id != opponent_id:
            opponent = User.query.filter(User.id == opponent_id).first()
            #if self pokemon > opponent pokemon (by length of names?), self win count +=1
            opp_score = []
            for pokemon in opponent.team:
                opp_points = pokemon.base_experience
                opp_score.append(opp_points)
            opp_final = sum(opp_score)
            my_score = []
            for pokemon in self.team:
                my_points = pokemon.base_experience
                my_score.append(my_points)
            my_final = sum(my_score)
            if my_final > opp_final:
                winner = self
                if self.wins is None:
                    self.wins = 0 
                self.wins += 1
                if opponent.losses is None:
                    opponent.losses = 0 
                opponent.losses += 1
                db.session.commit()
            else:
                winner = opponent
                if opponent.wins is None:
                    opponent.wins = 0 
                opponent.wins += 1
                if self.losses is None:
                    self.losses = 0 
                self.losses += 1
                db.session.commit()
            return winner


@login.user_loader
def load_user(id):
    return User.query.get(int(id))