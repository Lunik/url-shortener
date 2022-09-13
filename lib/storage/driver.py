import json
import io

from minio import Minio


class StorageDriver:
  def __init__(self,
    endpoint,
    access_key,
    secret_key,
    secure=True,
    region="default",
    bucket="urlshortener",
    prefix="",
  ):
    self.client = Minio(
      endpoint=endpoint,
      access_key=access_key,
      secret_key=secret_key,
      secure=secure,
      region=region,
    )

    if not self.client.bucket_exists(bucket):
      raise Exception(f"Bucket doesn't exists : {bucket}")
    self.bucket = bucket

    self.prefix = prefix


  def get_object(self, path):
    data = None

    response = self.client.get_object(self.bucket, f"{self.prefix}/{path}")

    content_type = response.getheader("content-type")

    data = response.read()
    if content_type == 'application/octet-stream':
      return data

    data = data.decode('utf8')
    if content_type == 'plain/text':
      return data

    data = json.loads(data)
    if content_type == 'application/json':
      return data

    raise Exception(f"Invalid data type : {content_type}")


  def put_object(self, path, data):
    content_type = None

    if type(data) == dict:
      data = json.dumps(data)
      content_type = content_type or 'application/json'

    if type(data) == str:
      data = data.encode('utf8')
      content_type = content_type or 'plain/text'

    if type(data) == bytes:
      content_type = content_type or 'application/octet-stream'
    else:
      raise Exception(f"Invalid data type : {type(data)}")

    result = self.client.put_object(
      self.bucket,
      f"{self.prefix}/{path}",
      io.BytesIO(data),
      len(data),
      content_type=content_type,
    )

    return result