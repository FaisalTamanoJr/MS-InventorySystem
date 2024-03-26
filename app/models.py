"""This module defines the structure of the database."""

import decimal
from typing import Optional
import sqlalchemy as sa  # For the database functions.
import sqlalchemy.orm as so  # Provides support for models.
from app import db, login
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Role(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True)

    # Links to the user table.
    users: so.WriteOnlyMapped['User'] = so.relationship(back_populates='role')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    fullname: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(11), unique=True)
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    birthday: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime)
    date_created: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    # Links to the login table.
    login: so.Mapped['Login'] = so.relationship(back_populates='user')

    # Links to the role table.
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Role.id), index=True)
    role: so.Mapped[Role] = so.relationship(back_populates='users')

    # Links to the transaction table.
    transactions: so.WriteOnlyMapped['Transaction'] = so.relationship(back_populates='user')

    # Links to the product table.
    products: so.WriteOnlyMapped['Product'] = so.relationship(back_populates='user')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<User {}>'.format(self.fullname)


# UserMixin includes safe implementations of the four requirements for flask-login to function
class Login(db.Model):
    username: so.Mapped[str] = so.mapped_column(sa.String(255), index=True, unique=True, primary_key=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(255))

    # Links to the user table.
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='login')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Login {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TransactionType(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True)

    # Links to the transaction table.
    transactions: so.WriteOnlyMapped['Transaction'] = so.relationship(back_populates='transaction_type')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<TransactionType {}>'.format(self.name)


class Transaction(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    total_amount_paid: so.Mapped[decimal] = so.mapped_column(sa.DECIMAL(precision=2))
    transaction_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    senior_citizen_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    senior_citizen_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))

    # Links to the user table.
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='transactions')

    # Links to the transaction type table.
    transaction_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(TransactionType.id), index=True)
    transaction_type: so.Mapped[TransactionType] = so.relationship(back_populates='transactions')

    # Links to the order table.
    orders: so.WriteOnlyMapped['Order'] = so.relationship(back_populates='transaction')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Transaction {}>'.format(self.id)


class ProductType(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True)

    # Links to the product table.
    products: so.WriteOnlyMapped['Product'] = so.relationship(back_populates='product_type')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<ProductType {}>'.format(self.name)


class Product(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True)
    price: so.Mapped[decimal] = so.mapped_column(sa.DECIMAL(precision=2))

    # Links to the stock table.
    stock: so.Mapped['Stock'] = so.relationship(back_populates='product')

    # Links to the user table.
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='products')

    # Links to the product type table.
    product_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(ProductType.id), index=True)
    product_type: so.Mapped[ProductType] = so.relationship(back_populates='products')

    # Links to the order table.
    orders: so.WriteOnlyMapped['Order'] = so.relationship(back_populates='product')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Product {}>'.format(self.name)


class Stock(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer)
    last_updated: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    # Links to the product table.
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Product.id), index=True)
    product: so.Mapped[Product] = so.relationship(back_populates='stock')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Stock {}>'.format(self.id)

    def edit_quantity(self, quantity):
        self.quantity = quantity
        self.last_updated = lambda: datetime.now(timezone.utc)


class Order(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer)
    total_price: so.Mapped[decimal] = so.mapped_column(sa.DECIMAL(precision=2))

    # Links to the transaction table.
    transaction_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Transaction.id), index=True)
    transaction: so.Mapped[Transaction] = so.relationship(back_populates='orders')

    # Links to the product table.
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Product.id), index=True)
    product: so.Mapped[Product] = so.relationship(back_populates='orders')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Order {}>'.format(self.id)


# This function will allow the Flask-login extension to load a user
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
