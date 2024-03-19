# my-tiny-url
Creates a tiny url for long urls and redirects to the original url when you use the tiny url

**Work-in-progress**

## Local setup

```sh
py -m venv venv
# activate venv
pip install poetry
poetry install
cd my_tiny_url
py app.py
# access app at http://localhost:8000
# access swagger ui at http://localhost:8000
# access swagger json at http://localhost:8000/swagger.json
```

## Swagger documentation

### `/create-url` (POST)
#### Summary:

Create a short URL

#### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| payload | body |  | Yes | [URLModel](#URLModel) |

#### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 201 | Success |
| 400 | Validation Error |

### `/{short_url}` (GET)
#### Summary:

Redirect to the long URL

#### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| short_url | path | The short URL identifier | Yes | string |

#### Responses

| Code | Description |
| ---- | ----------- |
| 301 | Redirect |
| 404 | URL Not Found |

### Models

#### URLModel

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| url | string | The long URL to be shortened | Yes |