import boto3
import os
import json
from typing import Dict, List

PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]
DELIVERIES_TABLE = os.environ["DELIVERIES_TABLE"]

dynamodb_client = boto3.client("dynamodb")


def handler(event: Dict, _):
    """Lambda handler function to process the DynamoDB stream events.

    Args:
        event (Dict): The DynamoDB stream event.
    """

    updated_data = event["Records"]
    for key in updated_data:
        if key["eventName"] == "INSERT":
            data = key["dynamodb"]["NewImage"]
            delivery = data["delivery"]["M"]
            products = data["products"]["L"]
            total = data["total"]["N"]

            post_products(products)
            post_delivery(delivery, len(products), float(total))


def post_delivery(delivery: Dict[str, str], n_products: int, total: float):
    """Post the delivery info and update deliveries performance (total
       money and delivered products) in the DELIVERIES_TABLE.

    Args:
        delivery (Dict[str,str]): Delivery info.
        n_products (int): Number of products in the order.
        total (float): Total money of the order.
    """
    
    delivery_id = delivery["delivery_id"]["N"]
    delivery_name = delivery["name"]["S"]

    response = dynamodb_client.get_item(
        TableName=DELIVERIES_TABLE, Key={"delivery_id": {"S": delivery_id}}
    )
    if "Item" not in response:
        # If the delivery does not exist, add it to the DELIVERIES_TABLE
        dynamodb_client.put_item(
            TableName=DELIVERIES_TABLE,
            Item={
                "delivery_id": {"S": delivery_id},
                "name": {"S": delivery_name},
                "delivered_products": {"N": str(n_products)},
                "total_money": {"N": str(total)},
            },
        )

    else:
        existing_deliveries = int(response["Item"]["delivered_products"]["N"])
        total_res = float(response["Item"]["total_money"]["N"])

        new_deliveries = existing_deliveries + n_products
        new_total = total + total_res

        dynamodb_client.update_item(
            TableName=DELIVERIES_TABLE,
            Key={"delivery_id": {"S": delivery_id}},
            UpdateExpression="SET delivered_products = :delivered_products, total_money = :new_total",
            ExpressionAttributeValues={
                ":delivered_products": {"N": str(new_deliveries)},
                ":new_total": {"N": str(new_total)},
            },
        )


def post_products(products: List[Dict]):
    """Post the products info and update the quantity in the PRODUCTS_TABLE.

    Args:
        products (List[Dict]): List of products in the order.
    """
    for product in products:
        product_id = product["M"]["id"]["S"]
        product_name = product["M"]["nombre"]["S"]

        response = dynamodb_client.get_item(
            TableName=PRODUCTS_TABLE, Key={"product_id": {"S": product_id}}
        )
  
        if not response.get("Item"):
            # If the product does not exist, add it to the PRODUCTS_TABLE
            dynamodb_client.put_item(
                TableName=PRODUCTS_TABLE,
                Item={
                    "product_id": {"S": product_id},
                    "name": {"S": product_name},
                    "quantity": {"N": "1"},
                },
            )

        else:

            existing_quantity = int(response["Item"]["quantity"]["N"])
            new_quantity = existing_quantity + 1

            dynamodb_client.update_item(
                TableName=PRODUCTS_TABLE,
                Key={"product_id": {"S": product_id}},
                UpdateExpression="SET quantity = :new_quantity",
                ExpressionAttributeValues={":new_quantity": {"N": str(new_quantity)}},
            )
