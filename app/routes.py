"""This module returns the appropriate webpage given a request/URL"""

from flask import render_template, flash, redirect, url_for
from app import app  # Import the app variable from the app package.
from app.forms import LoginForm

# Temporary mock variables
user = {'fullname': 'Juan Dela Cruz',
        'role': 'employee'}


# The decorators, or the code that starts with "@", are used for linking the URL given as an argument, and the function.
@app.route('/')
def index():
    if user['role'] == 'employee':
        return redirect(url_for('sales_register'))
    elif user['role'] == 'admin':
        return redirect(url_for('sales_report'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # If browser receives a POST request
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


# Sales
@app.route('/sales/register')
def sales_register():
    return render_template('sales_register.html', title='Sales Register', user=user)


@app.route('/sales/report')
def sales_report():
    return render_template('sales_report.html', title='Sales Report', user=user)


@app.route('/sales/trends')
def sales_trends():
    return render_template('sales_trends.html', title='Trends', user=user)


# Inventory
@app.route('/inventory')
def inventory():
    return render_template('inventory.html', title='Overall Inventory', user=user)


@app.route('/inventory/daily-report')
def inventory_daily_report():
    return render_template('inventory_daily_report.html', title='Daily Inventory Report', user=user)


# Accounts
@app.route('/accounts')
def accounts():
    return render_template('accounts.html', title='Accounts', user=user)


@app.route('/accounts/employee')
def accounts_employee():
    return render_template('accounts_employee.html', title='Employees', user=user)


@app.route('/accounts/admin')
def accounts_admin():
    return render_template('accounts_admin.html', title='Admins', user=user)
