"""This module returns the appropriate webpage given a request/URL."""

from flask import render_template, flash, redirect, url_for, request
from app import app  # Import the app variable from the app package.
from app.forms import LoginForm, AdminRegistrationForm, AccountCreationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Login, Role
from urllib.parse import urlsplit


# The decorators, or the code that starts with "@", are used for linking the URL given as an argument, and the function.
@app.route('/')
@login_required
def index():
    if db.session.scalars(sa.select(User)).first() is None:  # If there are no existing users, redirect to admin
        # registration page.
        return redirect(url_for('register_admin'))
    if current_user.role.name == 'employee':
        return redirect(url_for('sales_register'))
    elif current_user.role.name == 'admin':
        return redirect(url_for('sales_report'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if db.session.scalars(sa.select(User)).first() is None:  # If there are no existing users, redirect to admin
        # registration page.
        return redirect(url_for('register_admin'))
    if current_user.is_authenticated:  # Redirect to index if user is signed in already
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # If browser receives a POST request

        # Verify and sign in the user based on the provided data in the forms
        user = db.session.scalar(sa.select(User).where(User.login.has(Login.username == form.username.data)))  # Find
        # provided username in the database
        if user is None or not user.login.check_password(
                form.password.data):  # If user doesn't exist or password is wrong.
            flash('Enter a valid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)

        # Redirects to the next page. If a user opens a @login_required page but was not signed in, it redirects back
        # to that page after signing in.
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':  # The urlsplit is for determining whether the next
            # page url is a relative or absolute path (for security purposes)
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Sales
@app.route('/sales/register')
@login_required
def sales_register():
    return render_template('sales_register.html', title='Sales Register')


@app.route('/sales/report')
@login_required
def sales_report():
    return render_template('sales_report.html', title='Sales Report')


@app.route('/sales/trends')
@login_required
def sales_trends():
    return render_template('sales_trends.html', title='Trends')


# Inventory
@app.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html', title='Overall Inventory')


@app.route('/inventory/daily-report')
@login_required
def inventory_daily_report():
    return render_template('inventory_daily_report.html', title='Daily Inventory Report')


# Accounts
@app.route('/accounts')
@login_required
def accounts():
    return render_template('accounts.html', title='Accounts')


@app.route('/accounts/create-an-account', methods=['GET', 'POST'])
@login_required
def create_an_account():
    # Ensure the one creating an account is an admin, else redirect them to index
    if current_user.role.name != 'admin':
        return redirect(url_for('index'))

    form = AccountCreationForm()

    # If browser receives a POST request
    if form.validate_on_submit():
        # Register the user given the input provided and if it is valid.
        role = db.session.scalar(sa.select(Role).where(Role.name == form.role.data))
        user = User(fullname=form.fullname.data, phone=form.phone.data, email=form.email.data,
                    birthday=form.birthday.data, role=role)
        account_login = Login(username=form.username.data, user=user)
        account_login.set_password(form.password.data)
        db.session.add(user)
        db.session.add(account_login)
        db.session.commit()
        flash('Account has been Created.')

        return redirect(url_for('index'))

    return render_template('create_an_account.html', title='Create an Account', form=form)


@app.route('/accounts/employee')
@login_required
def accounts_employee():
    return render_template('accounts_employee.html', title='Employees')


@app.route('/accounts/admin')
@login_required
def accounts_admin():
    return render_template('accounts_admin.html', title='Admins')


@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = AdminRegistrationForm()

    # If browser receives a POST request
    if form.validate_on_submit():
        # Register the user given the input provided and if it is valid.
        role = Role(name='admin')
        user = User(fullname=form.fullname.data, phone=form.phone.data, email=form.email.data,
                    birthday=form.birthday.data, role=role)
        account_login = Login(username=form.username.data, user=user)
        account_login.set_password(form.password.data)
        db.session.add(role)
        db.session.add(user)
        db.session.add(account_login)
        db.session.commit()
        flash('Admin Account has been Created.')

        # Create the employee role in the database
        role = Role(name='employee')
        db.session.add(role)
        db.session.commit()

        return redirect(url_for('login'))

    # If a single user or more exist in the database, prevent them from accessing this page.
    if db.session.scalars(sa.select(User)).first() is not None:
        return redirect(url_for('index'))

    return render_template('register_admin.html', title='Admin Registration', form=form)
