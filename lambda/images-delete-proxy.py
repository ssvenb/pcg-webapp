import boto3

s3 = boto3.client("s3")
BUCKET = "pcg-images"


def lambda_handler(event, context):
    filename = event["path"].replace("/images/", "", 1)

    try:
        s3.delete_object(Bucket=BUCKET, Key=filename)
        return {"statusCode": 200}

    except s3.exceptions.NoSuchKey:
        return {"statusCode": 404, "body": "Not Found"}
