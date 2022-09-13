# URL Shortener

This project implement the basic functionalities of a URL shortener app using cloud functions

Exemple : https://p.vlx.ovh/tcnUQRMyeY

## Usage

```shell
python3 -m venv venv
source ./venv/bin/activate
pip3 install .
```

```shell
python3 functions/local/store.py <URL> [HASH]
```

```shell
python3 functions/local/retriev.py <HASH>
```

## Deploy

### Local test

```shell
docker-compose -f deploy/docker-compose.yml up -d
```

access : `minioadmin`:`minioadmin`

### Scaleway

```shell
./build.sh
```

#### `redirect` function

| Parameter | Value |
|:----------|:------|
| Code entry type | `ZIP` |
| Runtime         | Python `3.10` |
| Handler         | `functions/scaleway/retreiv.redirect` |

##### Environment vars

| Env | Value |
|:----|:------|
| `OS_RETREIV_HOSTNAME` | The endpoint hostname of the `retreiv` function |
| `OS_SECRET_TOKEN`     | Secret required for creating a new short URL |
| `OS_ENDPOINT`         | Object storage URL endpoint |
| `OS_REGION`           | Region of the object storage service |
| `OS_BUCKET`           | Name of the object storage bucket storing short URL configs |
| `OS_PREFIX`           | Prefix in the oject storage bucket |
| `OS_ACCESS_KEY`       | Access key for the object storage api |
| `OS_SECRET_KEY`       | Secret key for the object storage api |

#### `store` function

| Parameter | Value |
|:----------|:------|
| Code entry type | `ZIP` |
| Runtime         | Python `3.10` |
| Handler         | `functions/scaleway/store.save` |

##### Environment vars

| Env | Value |
|:----|:------|
| `OS_RETREIV_HOSTNAME` | The endpoint hostname of the `retreiv` function |
| `OS_SECRET_TOKEN`     | Secret required for creating a new short URL |
| `OS_ENDPOINT`         | Object storage URL endpoint |
| `OS_REGION`           | Region of the object storage service |
| `OS_BUCKET`           | Name of the object storage bucket storing short URL configs |
| `OS_PREFIX`           | Prefix in the oject storage bucket |
| `OS_ACCESS_KEY`       | Access key for the object storage api |
| `OS_SECRET_KEY`       | Secret key for the object storage api |