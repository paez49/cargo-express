import boto3
import os
import json

PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]
DELIVERIES_TABLE = os.environ["DELIVERIES_TABLE"]

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):

    updated_data = event["Records"]
    for key in updated_data:
        data = key["dynamodb"]["NewImage"]
        delivery = data["delivery"]["M"]
        products = data["products"]["L"]
        timestamp = data["timestamp"]["S"]
        post_products(products)
        post_delivery(delivery, len(products), timestamp)


def post_delivery(delivery, n_products, date):
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
                "timestamp": {"S": date},
            },
        )

    else:
        print(json.dumps(response))
        existing_deliveries = int(response["Item"]["delivered_products"]["N"])
        new_deliveries = existing_deliveries + n_products

        dynamodb_client.update_item(
            TableName=DELIVERIES_TABLE,
            Key={"delivery_id": {"S": delivery_id}},
            UpdateExpression="SET delivered_products = :delivered_products",
            ExpressionAttributeValues={
                ":delivered_products": {"N": str(new_deliveries)}
            },
        )


def post_products(products):
    for product in products:
        product_id = product["M"]["id"]["S"]
        product_name = product["M"]["nombre"]["S"]

        response = dynamodb_client.get_item(
            TableName=PRODUCTS_TABLE, Key={"product_id": {"S": product_id}}
        )

        if "Item" not in response:
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
            print(json.dumps(response))
            existing_quantity = int(response["Item"]["quantity"]["N"])
            new_quantity = existing_quantity + 1

            dynamodb_client.update_item(
                TableName=PRODUCTS_TABLE,
                Key={"product_id": {"S": product_id}},
                UpdateExpression="SET quantity = :new_quantity",
                ExpressionAttributeValues={":new_quantity": {"N": str(new_quantity)}},
            )
