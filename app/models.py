"""This module defines the structure of the database."""

from typing import Optional
import sqlalchemy as sa  # For the database functions.
import sqlalchemy.orm as so  # Provides support for models.
from app import db
from datetime import datetime, timezone


class Role(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255))

    # Links to the user table.
    users: so.WriteOnlyMapped['User'] = so.relationship(back_populates='role')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    fullname: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(11), unique=True)
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), unique=True)
    birthday: so.Mapped[Optional[datetime]] = so.mapped_column(sa.Date)
    date_created: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    # Links to the login table.
    login: so.Mapped['Login'] = so.relationship(back_populates='user')

    # Links to the role table.
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Role.id), index=True)
    role: so.Mapped[Role] = so.relationship(back_populates='users')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<User {}>'.format(self.fullname)


class Login(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(255), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(255))

    # Links to the user table.
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='login')

    # Tells how the object should be printed (for debugging purposes).
    def __repr__(self):
        return '<Login {}>'.format(self.username)

