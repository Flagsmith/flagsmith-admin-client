=======
# Flagsmith Admin API client

Python SDK for interacting with the Flagsmith Admin API.

## Local setup

```shell
poetry install
```

## Tests

```shell
poetry run pytest
```

## Examples

### Export features from all projects to CSV

```
export FLAGSMITH_TOKEN="..."
python examples/features-to-csv.py