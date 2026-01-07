from .models.main import Product
from .extensions import db
def get_list():
    numbers = range(1, 4)
    my_list = [[*numbers],[*numbers],[*numbers]]
    return my_list
def chunk_list(data, size):
    return [data[i:i + size] for i in range(0, len(data), size)]
def search(search_value):
    search_term = search_value
    products = Product.query.filter(Product.name.ilike(f"%{search_term}%")).all()
    
    return products

def calc_price(price, quantity):
    result = quantity * price
    return result


        
