import os

import boto3
from flask import Blueprint, jsonify, make_response, request
from collections import Counter
from datetime import datetime

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
    delivery_date_count = Counter()
    delivery_count_product = Counter()

    response = dynamodb_client.scan(TableName=ORDERS_TABLE) 

    items = response['Items']
    status_dict = {}
    if items:
        for item in items:
            products = item["products"]
            for product in products["L"]:
                product_data = product["M"]
                product_name = product_data["nombre"]["S"]
                product_count[product_name] += 1
            top_products = product_count.most_common(3)
            
            
            delivery_id = item['delivery']["M"]['delivery_id']['N']
            timestamp = item['timestamp']['S']
            hour = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').hour
            delivery_id_date = f"Delivery with id {delivery_id} deliver an order at {hour}"
            delivery_date_count[delivery_id_date] += 1
        
            delivery_id = item['delivery']["M"]['delivery_id']['N']
            products = item['products']['L']
            num_products = len(products)
            delivery_count_product[delivery_id] += num_products
            
            deliveries_with_more_products = sorted(delivery_count_product.items(), key=lambda x: x[1], reverse=True)[:3]
            
        status_dict["top_products"] = top_products
        status_dict["delivery_date_count"] = delivery_date_count
        status_dict["deliveries_with_more_products"] = deliveries_with_more_products

        
        return jsonify(status_dict)
    else:
        return jsonify({"error": "No orders registered"}), 404
