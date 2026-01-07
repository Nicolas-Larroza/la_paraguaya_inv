from flask import render_template, Blueprint, url_for, request, redirect
from app.services import chunk_list, search, calc_price
from app.models.main import Product
from app.extensions import db


main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    items = Product.query.all()
    return render_template("index.html", items=items)

@main_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
      return render_template("add.html")
    else:
        name = request.form.get("name")
        quantity= request.form.get("quantity", 0)
        price = request.form.get("price", 0)
        try:
            quantity = int(quantity)
            price = int(price)
        except ValueError:
            return "cantidad o precio invalido.", 400
        
        product = Product(name=name, quantity=quantity, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("main.home"))
    
@main_bp.route("/getselected", methods=["POST"])
def get_selected():
    if request.method == "POST":
        checked = request.form.getlist("selected[]")
        action = request.form.get("action")
        if len(checked) == 0:
            return "Asegurate de seleccionar lo que quieras editar antes de editarlo."
        products = []
        for id in checked:
            product = Product.query.get(id)
            if product is None:
                return "Producto no encontrado, algo salio mal.", 404
            print("product is the above.")
            products.append(product)
        
        if action == "edit":
            return render_template("edit.html",products=products)
        if action == "delete":
            for prdt in products:
                db.session.delete(prdt)
                db.session.commit()
                return redirect(url_for("main.home"))

@main_bp.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        ids = request.form.getlist("product_ids[]")
        product = request.form.get("product")
        for id in ids:
            product = Product.query.get(id)
            if not product:
                return "Producto no encontrado", 404
        product.name = request.form.get(f"name_{id}")
        product.quantity = int(request.form.get(f"quantity_{id}"))
        product.price = int(request.form.get(f"price_{id}"))
        
        db.session.commit()
        return redirect(url_for("main.home"))


class Sell_list():
    to_sell = []


@main_bp.route("/sell", methods=["GET", "POST"])
def sell():
    sell_list = Sell_list()
    if request.method == "GET":
        return render_template('sell.html')

    action = request.form.get('action')
    if action == 'search':
        search_value = request.form.get('search')
        searched_object = search(search_value)
        return render_template(
        'sell.html',
        results=searched_object)

    if action == 'add_to_sell_list':
        item_id = request.form.get('item_id')
        product = Product.query.get(item_id)
        sell_list.to_sell.append(product)
        return render_template('sell.html', to_sell=sell_list.to_sell)
    
    if action == 'sell':
        quantities = request.form.getlist('quantities[]')    
        ids = request.form.getlist('item_id[]')
        nmb_quantities = []
        for nmb in quantities:
            new_nmb = int(nmb)
            nmb_quantities.append(new_nmb)
    
        product_prices = []
        for id in ids:
            product = Product.query.get(id)
            if not product:
                return "Producto no encontrado", 404
            product_prices.append(product.price)
        
        price_of_bunch = []
        for price, quantity in zip(product_prices, nmb_quantities):
            final_price = calc_price(price, quantity)
            price_of_bunch.append(final_price)
        total = sum(price_of_bunch)
        sell_list.to_sell.clear()
            
        return render_template('sell.html', total=total)
            
    