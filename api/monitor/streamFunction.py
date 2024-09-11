import json
import os

PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]
DELIVERIES_TABLE = os.environ["DELIVERIES_TABLE"]

def handler(event, context):
    updated_data = event["NewImage"]
    delivery = updated_data["delivery"]["M"]
    products = updated_data["products"]["L"]
    