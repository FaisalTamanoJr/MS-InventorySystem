import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import Role, User, Login, TransactionType, Transaction, ProductType, Product, Stock, Order

app = create_app()

# Registers the items to the python interpreter session, making it not necessary to import everything in python
# interpreter manually (when ran using the flask shell command).
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Role': Role, 'User': User, 'Login': Login,
            'TransactionType': TransactionType, 'Transaction': Transaction, 'ProductType': ProductType,
            'Product': Product, 'Stock': Stock, 'Order': Order}
