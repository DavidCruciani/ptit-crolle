from ..db_class.db import User
from flask import Blueprint, render_template, redirect, url_for, request, flash
from .form import AddNewUserForm, LoginForm, EditUserFrom
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from . import account_core as AccountModel
from ..utils.utils import form_to_dict, redirect_to_home

account_blueprint = Blueprint(
    'account',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@account_blueprint.route("/")
@login_required
def index():
    return render_template("account/account_index.html", user=current_user)


@account_blueprint.route("/edit", methods=['GET', 'POST'])
@login_required
def edit_user():
    """Edit the user"""
    form = EditUserFrom()

    if form.validate_on_submit():
        form_dict = form_to_dict(form)
        user, message = AccountModel.edit_user_core(form_dict, current_user.id)
        if user:
            flash(message, "success")
        else:
            flash(message, "error")
        return redirect("/account")
    else:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    return render_template("account/edit_user.html", form=form)

@account_blueprint.route("/register", methods=['GET', 'POST'])
def create_user():
    """Edit the user"""
    form = AddNewUserForm()
    if form.validate_on_submit():
        form_dict = form_to_dict(form)

        if not current_user.is_admin():
            # if a non admin user creates a user, set the role to read only
            form_dict["role_id"] = 3
        user, message = AccountModel.create_user_core(form_dict)
        if user:
            flash(message, "success")
        else:
            flash(message, "error")
        return redirect("/account")
    return render_template("account/create_user.html", form=form)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'success')
            return redirect_to_home()
        else:
            flash('Invalid email or password.', 'error')
    return render_template('account/login.html', form=form)

@account_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect_to_home()

