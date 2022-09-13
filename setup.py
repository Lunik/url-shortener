from distutils.core import setup

setup(
  name='url-shortener',
  version='0.1.0',
  description='URL Shortener',
  author='Lunik',
  author_email='lunik@tiwabbit.fr',
  package_dir=dict(
    urlshortener='lib'
  ),
  install_requires=["minio"]
)