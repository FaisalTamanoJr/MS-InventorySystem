"""This module returns the appropriate webpage given a request/URL."""

from flask import render_template, flash, redirect, url_for, request
from app import app  # Import the app variable from the app package.
from app.forms import LoginForm, AdminRegistrationForm, AccountCreationForm, AddProductForm, AddProductTypeForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Login, Role, ProductType, Product, Stock, TransactionType, Transaction, Order
from urllib.parse import urlsplit
from dateutil import tz
from datetime import datetime, timezone


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
    products = db.session.scalars(sa.select(Product)).all()
    payment_methods = db.session.scalars(sa.select(TransactionType)).all()
    discount_percentage = 0.1

    # Get the transactions of current day
    current_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    transactions_today = db.session.scalars(sa.select(Transaction).where(Transaction.transaction_date >= current_datetime))
    transactions_today_list = []
    total_paid = 0
    total_quantity = 0
    for transaction in transactions_today:
        # Get transaction time
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = transaction.transaction_date
        utc = utc.replace(tzinfo=from_zone)
        transaction_time = utc.astimezone(to_zone)
        transaction_time = transaction_time.strftime("%H:%M")

        # Get transaction type
        transaction_type = db.session.scalar(sa.select(TransactionType.name).where(TransactionType.id == transaction.transaction_type_id))

        transaction_dict = {
            "time" : transaction_time,
            "orders" : [],
            "transaction_type" : transaction_type,
        }

        # Add to total paid
        total_paid += transaction.total_amount_paid

        # Add the orders to the transaction_dict, in a list and dictionary format
        orders = db.session.scalars(sa.select(Order).where(Order.transaction == transaction))
        for order in orders:
            product = db.session.scalar(sa.select(Product.name).where(Product.id == order.product_id))
            order_dict = {
                "product": product,
                "quantity": order.quantity,
                "total_price": round(order.total_price,2) }
            transaction_dict["orders"].append(order_dict)

            # Add to total quantity
            total_quantity += order.quantity

        transactions_today_list.append(transaction_dict)

    return render_template('sales_register.html', title='Sales Register', products=products,
                           payment_methods=payment_methods, discount=discount_percentage,
                           processed_transactions=transactions_today_list, total_paid=round(total_paid, 2),
                           total_quantity=total_quantity)


@app.route('/sales/register/process-transaction', methods=['POST'])
@login_required
def process_transaction():
    transaction_received = request.get_json(force=True)
    if transaction_received:
        # Transaction
        transaction_type = db.session.scalar(sa.select(TransactionType).where(TransactionType.name == transaction_received["transaction_type"]))
        transaction = Transaction(
            total_amount_paid = transaction_received['total_amount_paid'],
            senior_citizen_name = transaction_received['senior_citizen_name'],
            senior_citizen_id = transaction_received['senior_citizen_id'],
            gcash_ref_no = transaction_received['gcash_ref_no'],
            user = current_user,
            transaction_type = transaction_type
        )
        db.session.add(transaction)

        # Orders
        orders = transaction_received['orders']
        for o in orders:
            product = db.session.scalar(sa.select(Product).where(Product.name == o['product']))
            stock = db.session.scalar(sa.select(Stock).where(Stock.product_id == product.id))
            stock.quantity -= o['quantity']
            stock.last_updated = datetime.now(timezone.utc)

            if stock.quantity < 0:
                return product.name

            order = Order(
                quantity = o['quantity'],
                total_price = o['total_price'],
                transaction = transaction,
                product = product
            )
            db.session.add(order)

        # Submit to the database
        db.session.commit()
        flash('Transaction processed')
        return "success"

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


@app.route('/inventory/add-a-product', methods=['GET', 'POST'])
@login_required
def add_a_product():
    # Ensure the one creating an account is an admin, else redirect them to index
    if current_user.role.name != 'admin':
        return redirect(url_for('inventory'))

    form = AddProductForm()

    # If browser receives a POST request
    if form.validate_on_submit():
        # Add the product given the input provided and if it is valid.
        product_type = db.session.scalar(sa.select(ProductType).where(ProductType.name == form.type.data))
        product = Product(name=form.name.data, price=form.price.data, product_type=product_type, user=current_user)
        stock = Stock(quantity=form.stock.data, product=product)
        db.session.add(product)
        db.session.add(stock)
        db.session.commit()
        flash('Product has been Added')

        return redirect(url_for('inventory'))

    return render_template('inventory_add_a_product.html', title='Add a Product', form=form)


@app.route('/inventory/add-a-product-type', methods=['GET', 'POST'])
@login_required
def add_a_product_type():
    # Ensure the one creating an account is an admin, else redirect them to index
    if current_user.role.name != 'admin':
        return redirect(url_for('inventory'))

    form = AddProductTypeForm()

    # If browser receives a POST request
    if form.validate_on_submit():
        # Add the product given the input provided and if it is valid.
        product_type = ProductType(name=form.name.data)
        db.session.add(product_type)
        db.session.commit()
        flash('Product Type has been Added')

        return redirect(url_for('inventory'))

    return render_template('inventory_add_a_product_type.html', title='Add a Product Type', form=form)


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

        # Create the transaction types
        transaction_type = TransactionType(name='Cash')
        db.session.add(transaction_type)
        db.session.commit()
        transaction_type = TransactionType(name='GCash')
        db.session.add(transaction_type)
        db.session.commit()

        return redirect(url_for('login'))

    # If a single user or more exist in the database, prevent them from accessing this page.
    if db.session.scalars(sa.select(User)).first() is not None:
        return redirect(url_for('index'))

    return render_template('register_admin.html', title='Admin Registration', form=form)
