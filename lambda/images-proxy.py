import boto3
import json

s3 = boto3.client("s3")
BUCKET = "pcg-images"


def lambda_handler(event, context):
    path = event.get("path")
    try:
        if not path:
            response = s3.list_objects_v2(Bucket=BUCKET)
            objects = response.get("Contents", [])
            filenames = [obj["Key"] for obj in objects]
            return {"statusCode": 200, "body": json.dumps(filenames)}
        else:
            filename = path.replace("/images/", "", 1)
            presigned_url = s3.generate_presigned_url(
                "get_object", Params={"Bucket": BUCKET, "Key": filename}, ExpiresIn=600
            )
            return {"statusCode": 200, "body": json.dumps({"fetchUrl": presigned_url})}

    except s3.exceptions.NoSuchKey:
        return {"statusCode": 404, "body": "Not Found"}
