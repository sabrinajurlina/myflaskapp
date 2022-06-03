from flask import render_template, request, flash
import requests
from flask_login import login_required
from .forms import SearchForm
from .import bp as main
from app.models import Pokemon


@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@main.route('/build_team', methods=['GET', 'POST'])
@login_required
def build_team():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data
        search = Pokemon.query.filter_by(name = pokemon).first()
        if not search:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
            response = requests.get(url)
            if not response.ok:
                flash (f'We had an error on our end. Please try again.', 'danger')
                return render_template('build_team.html.j2', form=form)
            
            if not response.json()['name']:
                flash(f'We had an error loading your data. Check your spelling, or maybe that pokemon does not exist.', 'danger')
                return render_template('build_team.html.j2', form=form)

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
            search = Pokemon()
            search.from_dict(poke_dict)
            search.save()

        return render_template('build_team.html.j2', form=form, pokemon=search)

    return render_template('build_team.html.j2', form=form)
