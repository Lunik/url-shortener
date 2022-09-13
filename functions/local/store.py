import os
import sys

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

  if len(sys.argv) > 3 or len(sys.argv) <= 1:
    raise Exception("Usage: <URL> [HASH]")

  params = sys.argv[1:]
  
  print(shortener.put_url(*params))
