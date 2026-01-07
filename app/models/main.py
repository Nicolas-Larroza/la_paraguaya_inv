from app.extensions import db
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default = 0)
    price = db.Column(db.Integer, default = 0)
    def __str__(self):
        return f"<product: {self.name}>"