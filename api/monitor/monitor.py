import os

import boto3
from flask import Blueprint, jsonify, make_response, request
from collections import Counter



dynamodb_client = boto3.client("dynamodb")

if os.environ.get("IS_OFFLINE"):
    dynamodb_client = boto3.client(
        "dynamodb", region_name="localhost", endpoint_url="http://localhost:8000"
    )

monitor_bp = Blueprint("monitor", __name__)

ORDERS_TABLE = os.environ["ORDERS_TABLE"]


@monitor_bp.route("/monitor/status", methods=["GET"])
def get_data():
    product_count = Counter()
    
    response = dynamodb_client.scan(TableName=ORDERS_TABLE)
    items = response.get('Items', [])
    if items:
        for record in items:
            products = record.get('products', [])
            for product in products["L"]:
                product_data = product.get('M', {})
                product_name = product_data.get('nombre', {}).get('S', '')
                product_count[product_name] += 1
        
        top_products = product_count.most_common(3)
        return jsonify(top_products)
    else:
        jsonify({"error": "No orders registered"}), 404
