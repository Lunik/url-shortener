import os
import sys
from minio.error import S3Error

from urlshortener.storage import StorageDriver
from urlshortener.shortener import Shortener

if __name__ == '__main__':
  driver = StorageDriver(
    os.environ.get('endpoint'),
    os.environ.get('access_key'),
    os.environ.get('secret_key'),
    os.environ.get('secure', False) in ['true', 'True'],
    os.environ.get('region', 'default'),
    os.environ.get('bucket', 'url-shortener'),
    os.environ.get('prefix', 'localtest'),
  )

  shortener = Shortener(driver)

  try:
    print(shortener.get_url(sys.argv[1]))
  except S3Error as error:
    raise error