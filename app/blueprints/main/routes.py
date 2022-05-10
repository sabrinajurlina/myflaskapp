from flask import render_template, request
import requests
from flask_login import login_required
from .forms import SearchForm
from .import bp as main


@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@main.route('/pokeinfo', methods=['GET', 'POST'])
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