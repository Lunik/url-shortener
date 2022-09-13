import hashlib
import base64

class Shortener:
  def __init__(self, storage_driver, hash_size=10):
    self.storage_driver = storage_driver
    self.hash_size = hash_size

  def generate_hash(self, data):
    hash_data = hashlib.sha224(data.encode('utf8')).digest()
    base64_hash = base64.b64encode(hash_data)[:self.hash_size]

    sanitized_hash = base64_hash.decode('utf8').replace('/', '_').replace('+', '-')

    return sanitized_hash

  def get_url(self, url_hash):
    url_hash = url_hash[:self.hash_size]

    data = self.storage_driver.get_object(
      f"{url_hash[:2]}/{url_hash[2:4]}/{url_hash}",
    )

    return data

  def put_url(self, url, url_hash=None):
    if url_hash and len(url_hash) >= 4:
      url_hash = url_hash[:self.hash_size]
    else:
      url_hash = self.generate_hash(url)

    data = dict(url=url)

    self.storage_driver.put_object(
      f"{url_hash[:2]}/{url_hash[2:4]}/{url_hash}",
      data,
    )

    return url_hash