'''This module returns the appropriate webpage given a request/URL'''

from flask import render_template
from app import app  # Import the app variable from the app package.

# Temporary mock variables
user = {'username': 'Juan Dela Cruz'}
transactions = [
    {
        'time' : '7:18 PM',
        'item' : 'Chicken',
        'order_count': '5',
        'MOP' : 'Cash',
        'amount' : '1000 PHP',
    },
    {
        'time': '8:18 AM',
        'item': 'Beef',
        'order_count': '3',
        'MOP': 'Cash',
        'amount': '700 PHP',
    }
]

# The decorators, or the code that starts with "@", are used for linking the URL given as an argument, and the function.
@app.route('/')
def index():
    return render_template('index.html', title='Home', user=user, transactions=transactions)


@app.route('/login')
def login():
    print("login")
