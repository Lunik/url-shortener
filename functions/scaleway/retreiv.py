import json
import os

from minio.error import S3Error

from urlshortener.storage import StorageDriver
from urlshortener.shortener import Shortener

def redirect(event, context):
  try:
    print(event)

    driver = StorageDriver(
      os.environ.get('OS_ENDPOINT'),
      os.environ.get('OS_ACCESS_KEY'),
      os.environ.get('OS_SECRET_KEY'),
      True,
      os.environ.get('OS_REGION'),
      os.environ.get('OS_BUCKET'),
      os.environ.get('OS_PREFIX'),
    )

    shortener = Shortener(driver)

    hash_url = event['path'].split('/')[1]

    redirect_url = shortener.get_url(hash_url)['url']
  except S3Error as error:
    match error.code:
      case "NoSuchKey":
        return { "body": "Invalid URL", "statusCode": 404 }

      case _:
        raise error

  except Exception as error:
    print(error)
    return { "statusCode": 500 }
  
  return {
    "body": f"Redirecting to : {redirect_url}",
    "headers": {
      "location": redirect_url
    },
    "statusCode": 301,
  }
