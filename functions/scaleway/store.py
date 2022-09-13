import json
import os
from urllib.parse import parse_qs

from minio.error import S3Error

from urlshortener.storage import StorageDriver
from urlshortener.shortener import Shortener

def get_html():
  return """
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf8">
    <meta name="viewport" content="initial-scale=1">
    <title>URL Shortener</title>
  </head>
  <body>
    <form action="/" method="post">
      <label for="secret">Secret :</label>
      <input id="secret" type="password" name="secret" required>
      <br>
      <label for="url">URL :</label>
      <input id="url" type="url" name="url" required>
      <br>
      <label for="hash">Hash :</label>
      <input id="hash" type="text" name="hash">
      <br>
      <input type="submit">
    </form>
  </body>
  </html>
  """

def save(event, context):
  try:
    print(event)

    if event['httpMethod'] == "GET":
      return {
        "body": get_html(),
        "statusCode": 200
      }

    secret_token = os.environ.get('OS_SECRET_TOKEN')

    form = parse_qs(event['body'])

    if form.get('secret', [None])[0] != secret_token:
       return { "body": "Invalid token", "statusCode": 403 }

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

    url = form.get('url', [None])[0]
    hash_url = form.get('hash', [None])[0]

    hash_url = shortener.put_url(url, hash_url)
  except Exception as error:
    print(error)
    return { "statusCode": 500 }

  return {
    "body": {
      "hash": hash_url,
      "url": f"https://{os.environ.get('OS_RETREIV_HOSTNAME')}/{hash_url}",
      "target": url
    },
    "statusCode": 200
  }
