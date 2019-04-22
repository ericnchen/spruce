# -*- coding: utf-8 -*-

# $ docker run -p 8000:8000 amazon/dynamodb-local

# https://stackoverflow.com/questions/31288085/how-to-append-a-value-to-list-attribute-on-aws-dynamodb


def test_build_mock_database_sets_up_dynamodb_correctly():
    import uuid
    import boto3

    db = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="test",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

    table_kwargs = {
        "TableName": "plants",
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
            {"AttributeName": "name", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "name", "AttributeType": "S"},
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }

    try:
        table = db.create_table(**table_kwargs)
    except db.meta.client.exceptions.ResourceInUseException:
        table = db.Table(table_kwargs["TableName"])

    table.meta.client.get_waiter("table_exists").wait(TableName="plants")

    dummy_item = {
        "id": str(uuid.uuid4()),
        "name": "Monstera Deliciosa",
        "common_name": "Monstera Deliciosa",
        "scientific_name": "Monstera deliciosa",
        "date_added": "2019-01-30T18:51:44.362243",
        "date_purchased": "2019-01-30T18:51:44.362243",
    }

    table.put_item(Item=dummy_item)

    response = table.scan()

    # response = table.get_item(
    #     Key={
    #         "id": _id,
    #         "name": "Monstera Deliciosa",
    #     }
    # )

    import pprint

    pprint.pprint(response)

    # assert response['Item'] == dummy_item
