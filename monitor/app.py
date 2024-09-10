import os

import boto3
from flask import Flask, jsonify, make_response, request
from collections import Counter
app = Flask(__name__)


dynamodb_client = boto3.client("dynamodb")

if os.environ.get("IS_OFFLINE"):
    dynamodb_client = boto3.client(
        "dynamodb", region_name="localhost", endpoint_url="http://localhost:8000"
    )


ORDERS_TABLE = os.environ["ORDERS_TABLE"]


@app.route("/data", methods=["GET"])
def get_data():
    product_count = Counter()
    
    response = dynamodb_client.scan(TableName=ORDERS_TABLE)
        
    for record in response:
        products = record.get('products', [])
        for product in products:
            product_id = product.get('IdProduct', '')
            product_count[product_id] += 1
    
    top_products = product_count.most_common(3)
    return jsonify(top_products)

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
