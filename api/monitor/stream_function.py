import boto3
import os
import json

PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]
DELIVERIES_TABLE = os.environ["DELIVERIES_TABLE"]

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):

    updated_data = event["Records"]
    print(updated_data)
    for key in updated_data:
        if key["eventName"] == "INSERT":
            data = key["dynamodb"]["NewImage"]
            delivery = data["delivery"]["M"]
            products = data["products"]["L"]
            total = data["total"]["N"]
            post_products(products)
            post_delivery(delivery, len(products), float(total))


def post_delivery(delivery, n_products, total):
    delivery_id = delivery["delivery_id"]["N"]
    delivery_name = delivery["name"]["S"]

    response = dynamodb_client.get_item(
        TableName=DELIVERIES_TABLE, Key={"delivery_id": {"S": delivery_id}}
    )
    print("### Response delivery")
    print(json.dumps(response))
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
        print(json.dumps(response))
        existing_deliveries = int(response["Item"]["delivered_products"]["N"])
        total_res = float(response["Item"]["total_money"]["N"])
        new_deliveries = existing_deliveries + n_products
        new_total = total + total_res
        print(new_total)
        dynamodb_client.update_item(
            TableName=DELIVERIES_TABLE,
            Key={"delivery_id": {"S": delivery_id}},
            UpdateExpression="SET delivered_products = :delivered_products, total_money = :new_total",
            ExpressionAttributeValues={
                ":delivered_products": {"N": str(new_deliveries)},
                ":new_total": {"N": str(new_total)},
            },
        )


def post_products(products):
    print("### Products")
    print(products)
    for product in products:
        product_id = product["M"]["id"]["S"]
        product_name = product["M"]["nombre"]["S"]

        response = dynamodb_client.get_item(
            TableName=PRODUCTS_TABLE, Key={"product_id": {"S": product_id}}
        )
        print("### Response products")
        print(json.dumps(response))
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
