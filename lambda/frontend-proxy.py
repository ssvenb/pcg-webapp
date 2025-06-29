import boto3
import mimetypes

s3 = boto3.client("s3")
BUCKET = "pcg-frontend"


def lambda_handler(event, context):
    path = event["path"].replace("/files/", "", 1)
    if not path:
        path = "index.html"

    try:
        response = s3.get_object(Bucket=BUCKET, Key=path)
        content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": content_type, "Cache-Control": "max-age=3600"},
            "body": (response["Body"].read().decode("utf-8") if "text" in content_type else response["Body"].read()),
            "isBase64Encoded": False if "text" in content_type else True,
        }

    except s3.exceptions.NoSuchKey:
        return {"statusCode": 404, "body": "Not Found"}
