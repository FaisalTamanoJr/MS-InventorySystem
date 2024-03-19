"""This module returns the appropriate webpage given a request/URL."""

from flask import render_template, flash, redirect, url_for, request
from app import app  # Import the app variable from the app package.
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Login
from urllib.parse import urlsplit

# The decorators, or the code that starts with "@", are used for linking the URL given as an argument, and the function.
@app.route('/')
@login_required
def index():
    if current_user.role.name == 'employee':
        return redirect(url_for('sales_register'))
    elif current_user.role.name == 'admin':
        return redirect(url_for('sales_report'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Redirect to index if user is signed in already
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # If browser receives a POST request

        # Verify and sign in the user based on the provided data in the forms
        user = db.session.scalar(sa.select(User).where(User.login.has(Login.username == form.username.data)))  # Find provided
        # username in the database
        print(user)
        if user is None or not user.login.check_password(
                form.password.data):  # If user doesn't exist or password is wrong.
            flash('Enter a valid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)

        # Redirects to the next page. If a user opens a @loginrequired page but was not signed in, it redirects back
        # to that page after signing in.
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '': # The urlsplit is for determining whether the next
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


@app.route('/accounts/employee')
@login_required
def accounts_employee():
    return render_template('accounts_employee.html', title='Employees')


@app.route('/accounts/admin')
@login_required
def accounts_admin():
    return render_template('accounts_admin.html', title='Admins')


@app.route('/register_admin')
def register_admin():
    return render_template('register_admin.html', title='Admin Registration')
