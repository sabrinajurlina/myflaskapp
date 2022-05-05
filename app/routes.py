from flask import render_template, request, flash, url_for
import requests
from .forms import LoginForm, SearchForm, RegisterForm
from app import app
from .models import User
from flask_login import current_user, login_user, login_required

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name" : form.first_name.data.title(),
                "last_name" : form.last_name.data.title(), 
                "email" : form.email.data.lower(),
                "password" : form.password.data
            }

            #creates empty User
            new_user_object = User()
            #builds user with their form inputs
            new_user_object.from_dict(new_user_data)
            #saves to db
            new_user_object.save()
        except:
            flash("There was an unexpected Error when creating your account. Please try again", "danger")
            return render_template('register.html.j2', form=form)
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get("REGISTERED_USERS") and password == app.config.get("REGISTERED_USERS").get(email).get('password'):
            return f"Welcome {app.config.get('REGISTERED_USERS').get(email).get('name')}"
        error_string = "Incorrect Email & Password Combination"
        return render_template("login.html.j2", error=error_string, form=form)
    
    return render_template("login.html.j2", form=form)

@app.route('/pokeinfo', methods=['GET', 'POST'])
@login_required
def pokeinfo():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = requests.get(url)
        if not response.ok:
            error_string = 'We had an error'
            return render_template('pokeinfo.html.j2', form=form, error=error_string)
        
        if not response.json()['name']:
            error_string = 'We had an error loading your data. Check your spelling, or maybe that pokemon does not exist.'
            return render_template('pokeinfo.html.j2', form=form, error=error_string)

        poke = response.json()
        poke_dict={
            "name":poke['name'],
            "base_experience":poke['base_experience'],
            "hp":poke['stats'][0]['base_stat'],
            "attack":poke['stats'][1]['base_stat'],
            "defense":poke['stats'][2]['base_stat'],
            "ability":poke['abilities'][0]['ability']['name'],
            "sprite":poke['sprites']['front_default'],
        }
        return render_template('pokeinfo.html.j2', form=form, pokemon=poke_dict)

    return render_template('pokeinfo.html.j2', form=form)