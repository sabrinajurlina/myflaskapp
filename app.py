from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokeinfo', methods=['GET', 'POST'])
def pokeinfo():
    if request.method == 'POST':
        name = request.form.get('name')

        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        if not response.ok:
            error_string = 'We had an error'
            return render_template('pokeinfo.html.j2', error=error_string)
        
        if not response.json()['name']:
            error_string = 'We had an error loading your data. Check your spelling, or maybe that pokemon does not exist.'
            return render_template('pokeinfo.html.j2', error=error_string)

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

        return render_template('pokeinfo.html.j2', pokemon=poke_dict)

    return render_template('pokeinfo.html.j2')