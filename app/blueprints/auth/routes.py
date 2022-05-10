from flask import render_template, request, flash, redirect, url_for
from .forms import EditProfileForm, LoginForm, RegisterForm
from .import bp as auth
from ...models import User
from flask_login import current_user, login_user, login_required, logout_user


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name" : form.first_name.data.title(),
                "last_name" : form.last_name.data.title(), 
                "email" : form.email.data.lower(),
                "password" : form.password.data,
                "icon" : f'{form.first_name.data.title()} {form.last_name.data.title()}'
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
        return redirect(url_for('auth.login')) #url_for lives in jinja, so we have to import it in python
    return render_template('register.html.j2', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Pokemon Pals!', 'success')
            return redirect(url_for('main.index'))

        flash("Incorrect Email & Password Combination", 'danger')
        return render_template("login.html.j2", form=form)
    return render_template("login.html.j2", form=form)

@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method=='POST' and form.validate_on_submit():
        new_user_data={"first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(), 
                "email": form.email.data.lower(),
                "password": form.password.data,
                "icon": form.icon
            }
        user = User.query.filter_by(email=new_user_data["email"]).first() #only going to be one!
        if user and user.email != current_user.email:
            flash('Email is already in use', 'danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Your profile has been updated', 'success')
        except:
            flash('Their was an unexpected error updating your profile', 'danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))
    return render_template('register.html.j2', form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('auth.login'))