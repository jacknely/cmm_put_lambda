import pytest
from pathlib import Path
import sys
from unittest.mock import patch
import boto3
from moto import mock_dynamodb2, mock_s3
import os

# needs set as PYTHONPATH env unav
sys.path.insert(0, str(Path(__file__).parent) + "/../")

from handler import insert_into_db, extract_file_data

class TestHandler:

    @mock_s3
    def test_extract_file_data(self):
        s3 = boto3.client('s3', region_name='eu-west-1')
        test_file = "data_sample.ACTL"
        test_bucket = "cmm-filtered"
        s3.create_bucket(Bucket=test_bucket)
        test_path = Path(__file__).parent / f"test_data/{test_file}"
        with open(test_path, "rb") as file:
            s3.upload_fileobj(file, test_bucket, test_file)

        s3 = boto3.resource("s3")
        obj = s3.Object(test_bucket, test_file)
        raw_data = extract_file_data(obj)

        assert len(raw_data) == 34

    @mock_dynamodb2
    def test_insert_into_db(self):
        # moto doesnt want to work without below env vars
        os.environ["AWS_ACCESS_KEY_ID"] = "foo"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "bar"
        os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
        table_name = "cmm.results"
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")

        # create a mock dynamodb table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"},],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"},],
        )

        point_data = [{
            "id": {"S": "test123"},
            "point": {"S": "test1"},
            "program_id": {"S": "test1"},
            "part_number": {"S": "test1"},
            "filename": {"S": "test1"},
            "date": {"S": "test1"},
            "time": {"S": "test1"},
            "x": {"S": "test1"},
            "y": {"S": "test1"},
            "z": {"S": "test1"},
            "nominal": {"S": "test1"},
            "lsl": {"S": "test1"},
            "usp": {"S": "test1"},
            "i": {"S": "test1"},
            "j": {"S": "test1"},
            "k": {"S": "test1"},
            "k": {"S": "test1"},
            "actual": {"S": "test1"},
            "dev": {"S": "test1"},

        }]

        insert_into_db(point_data)

        table = dynamodb.Table(table_name)
        response = table.get_item(Key={"id": "test123"})
        if "Item" in response:
            item = response["Item"]

        assert "id" in item
        assert item["id"] == "test123"
