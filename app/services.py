from .models.main import Product
from .extensions import db

def search(search_value):
    search_terms = search_value.split()
    query = Product.query
    for term in search_terms:
        query = query.filter(Product.name.ilike(f"%{term}%"))
    result = query.all()
    return result

def calc_price(price, quantity):
    result = quantity * price
    return result


        
