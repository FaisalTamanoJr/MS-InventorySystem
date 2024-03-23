"""This module will store all web form classes found in the webapp."""

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, DecimalField, IntegerField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Optional, Email, Length, ValidationError
from app import db
from app.models import Role, User, Login, ProductType, Product, TransactionType

class LoginForm(FlaskForm):
    username = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AdminRegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=11, max=11)])
    email = StringField('Email (Optional)', validators=[Optional(), Email()])
    birthday = DateField('Birthday (Optional)', validators=[Optional()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class AccountCreationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=11, max=11)])
    email = StringField('Email (Optional)', validators=[Optional(), Email()])
    birthday = DateField('Birthday (Optional)', validators=[Optional()])
    role = SelectField('Role', validators=[DataRequired()],
                       choices=lambda: db.session.scalars(sa.select(Role.name)).all())
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user_username = db.session.scalar(sa.select(Login).where(Login.username == username.data))
        if user_username is not None:
            raise ValidationError('Please use a different username.')

    def validate_phone(self, phone):
        user_phone = db.session.scalar(sa.select(User).where(
            User.phone == phone.data))
        if user_phone is not None:
            raise ValidationError('Please use a different phone number.')

    def validate_email(self, email):
        user_email = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user_email is not None:
            raise ValidationError('Please use a different email address.')


class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    type = SelectField('Product Type', validators=[DataRequired()],
                       choices=lambda: db.session.scalars(sa.select(ProductType.name)).all())
    price = DecimalField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    submit = SubmitField('Add Product')


class AddProductTypeForm(FlaskForm):
    name = StringField('Product Type Name', validators=[DataRequired()])
    submit = SubmitField('Add Product Type')


class AddOrderForm(FlaskForm):
    product = SelectField('Product', validators=[DataRequired()],
                          choices=lambda: db.session.scalars(sa.select(Product.name)).all())
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('+')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class TransactionForm(FlaskForm):
    payment_method = SelectField('Mode of Payment: ', validators=[DataRequired()],
                       choices=lambda: db.session.scalars(sa.select(TransactionType.name)).all())
    discount = BooleanField('PWD/Senior Discount? ')
    order_checkbox_field = MultiCheckboxField('Orders')
    remove_items_submit = SubmitField('Remove Order(s)')
    process_submit = SubmitField('Process')

    def set_order_checkbox_items(self, orders):
        list_of_orders = [(orders.index(order), order["product"].name) for order in orders]
        self.order_checkbox_field.choices = list_of_orders
