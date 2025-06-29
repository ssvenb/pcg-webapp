import json
import boto3
import uuid

s3 = boto3.client("s3")
BUCKET_NAME = "pcg-images"
EXPIRES_IN = 300


def lambda_handler(event, context):
    try:
        file_name = str(uuid.uuid4()) + ".jpg"
        content_type = "image/jpeg"

        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": file_name,
                "ContentType": content_type,
            },
            ExpiresIn=EXPIRES_IN,
            HttpMethod="PUT",
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"uploadUrl": presigned_url, "fileName": file_name}),
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
