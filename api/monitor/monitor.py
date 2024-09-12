import os

import boto3
from flask import Blueprint, jsonify, make_response, request
from typing import Dict

dynamodb_client = boto3.client("dynamodb")

if os.environ.get("IS_OFFLINE"):
    dynamodb_client = boto3.client(
        "dynamodb", region_name="localhost", endpoint_url="http://localhost:8000"
    )

monitor_bp = Blueprint("monitor", __name__)

PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]
DELIVERIES_TABLE = os.environ["DELIVERIES_TABLE"]


@monitor_bp.route("/monitor/status", methods=["GET"])
def get_data() -> Dict[str, Dict[str, str]]:
    """Get the status of the products and deliveries.

    Returns:
        Dict[str,Dict[str,str]]: Product sales and delivery performance.
    """
    response_products = dynamodb_client.scan(TableName=PRODUCTS_TABLE)
    response_deliveries = dynamodb_client.scan(TableName=DELIVERIES_TABLE)

    items_products = response_products["Items"]
    items_deliveries = response_deliveries["Items"]
    status_dict = {}

    if items_products or items_deliveries:
        status_dict["products_sales"] = items_products
        status_dict["delivery_performance"] = items_deliveries
        return jsonify(status_dict)
    else:
        return jsonify({"error": "No orders registered"}), 404
