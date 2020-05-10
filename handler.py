#!/usr/bin/env python

import json
import boto3
from botocore.exceptions import ClientError
import csv

s3 = boto3.resource("s3")
dynamodb = boto3.client("dynamodb")
table_name = "cmm.results"


def insert_into_db(point_data, overwrite: bool = False) -> None:
    """
    inserts jobs to aws dynamodb
    :params set to True to overwrite values in DB
    if key exists
    """
    condition = f"attribute_not_exists(id)"
    for point in point_data[:5]:
        try:
            if overwrite:
                condition = f"attribute_not_exists(f.id)"
            response = dynamodb.put_item(
                TableName=table_name, Item=point,
                ConditionExpression=condition
            )
        except ClientError as error:
            print(f"Unexpected error: {error}")
    print(f"SUCCESS: Data inserted to {table_name}")

def get_event_details(event) -> tuple:
    """
    extract infomation from trigger
    event
    :param aws event
    :return bucket str
    :return key str
    """
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    return bucket, key


def extract_file_data(obj):
    """
    takes a cmm file and extracts data
    to be a list of line items
    :params obj as s3 object
    :return lost of lines in file
    """
    content = obj.get()["Body"].read().decode("utf-8").splitlines()
    reader = csv.reader(content)
    raw_data = list(reader)

    return raw_data


def parse_data(raw_data: list) -> list:
    """
    returns a list of dicts for each point
    with data to be moved into db
    """
    points = []
    for index, item in enumerate(raw_data[32], start=3):
        if index >= len(raw_data[32]):
            break
        point_data = make_db_schema(raw_data, index)
        points.append(point_data)

    return points


def make_db_schema(raw_data, index):
    """
    parsing schema for .ACTL files
    which are output from CMM
    """
    point_data = {
        "id": {"S": raw_data[32][index] + "_"
         + raw_data[33][1]},
        "point": {"S": raw_data[32][index]},
        "program_id": {"S": raw_data[1][1]},
        "part_number": {"S": raw_data[3][1] or "null"},
        "filename": {"S": raw_data[33][0]},
        "date": {"S": raw_data[33][1]},
        "time": {"S": raw_data[33][2]},
        "x": {"S": raw_data[9][index]},
        "y": {"S": raw_data[10][index]},
        "z": {"S": raw_data[11][index]},
        "nominal": {"S": raw_data[12][index]},
        "lsl": {"S": raw_data[13][index]},
        "usp": {"S": raw_data[14][index]},
        "i": {"S": raw_data[15][index]},
        "j": {"S": raw_data[16][index]},
        "k": {"S": raw_data[17][index]},
        "k": {"S": raw_data[17][index]},
        "actual": {"S": raw_data[33][index]},
        "dev": {"S": str(round(float(raw_data[33][index]) -
                    float(raw_data[12][index]), 3))},

    }

    return point_data


def lambda_handler(event, context):
    """
    event handlered triggered by S3 put
    """
    bucket, key = get_event_details(event)
    obj = s3.Object(bucket, key)
    raw_data = extract_file_data(obj)
    parsed_data = parse_data(raw_data)
    insert_into_db(parsed_data, overwrite=True)

    return {"statusCode": 200, "body": "Upload Complete"}


if __name__ == "__main__":
    bucket = "cmm-filtered"
    key = "ACCUM_008.RES.ACTL"
    obj = s3.Object(bucket, key)
    raw_data = extract_file_data(obj)
    parsed_data = parse_data(raw_data)
    insert_into_db(parsed_data, overwrite=True)
