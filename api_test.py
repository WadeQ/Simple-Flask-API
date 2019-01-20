from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init database
db = SQLAlchemy(app)

# init marshmallow
marshmallow = Marshmallow(app)


# our class here
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class ProductSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)


# create product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)

    # add product to db
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# retrieve product
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = product_schema.dump(all_products)
    return jsonify(result.data)


# retrieve a single product
@app.route('/product<id>', methods=['GET'])
def get_single_product(id):
    single_product = Product.query.get(id)
    return product_schema.jsonify(single_product)


# update our product schema
@app.route('/product<id>', methods=['PUT'])
def update_product(id):
    updated_product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    updated_product.name = name
    updated_product.description = description
    updated_product.price = price
    updated_product.quantity = quantity

    # commit changes to db
    db.session.commit()

    return product_schema.jsonify(updated_product)


# delete product
@app.route('/product<id>', methods=['DELETE'])
def delete_product():
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(product)


if __name__ == '__main__':
    app.run(debug=True)
