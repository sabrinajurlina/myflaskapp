from .import bp as game
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Pokemon, PokemonUser


@game.route('/catch/<string:name>')
# methods=['GET', 'POST']?
@login_required
def catch(name):
    print(current_user.team, 'CURRENT TEAM')
    poke=Pokemon.query.filter_by(name = name).first()
    if current_user.team.count()==5:
        flash(f"Your team is full! Please either delete a Pokemon or play with your current team", 'danger')
        return redirect(url_for("main.build_team"))
    else:
        current_user.catch_poke(poke)
        flash(f"Congrats! You caught {name.title()}", "success")
        return redirect(url_for("game.show_team"))


@game.route('/delete/<string:name>')
@login_required
def delete(name):
    poke=Pokemon.query.filter_by(name = name).first()
    Pokemon.delete(poke)
    flash(f"{name.title()} has been deleted from your team", "warning")
    return redirect(url_for("main.build_team"))


@game.route('/show_team')
@login_required
def show_team():
    # show current user's team of pokemon
    team = current_user.show_team()
    return render_template('show_team.html.j2', team=team)


@game.route('/show_players')
@login_required
def show_players():
    players = current_user.show_players()
    return render_template('show_players.html.j2', players=players)


@game.route('/battle/<int:id>')
@login_required
def battle(id):
    winner = current_user.battle(id)
    return render_template('battle.html.j2', winner=winner)
