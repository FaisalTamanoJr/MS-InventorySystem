from app.models import Product


def create_order_dictionary(product, quantity):  # Adds an order to a dictionary
    order = {
        "product": product,
        "quantity": quantity,
        "total_price": product.price * quantity
    }
    return order


def delete_item_at_indices(given_list, indices):
    for index in indices:
        given_list.pop(index)
    return given_list
