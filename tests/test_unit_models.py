from flagsmith_admin_client.models import Feature


def test_feature() -> None:
    assert Feature.model_validate({"id": 1, "name": "foo"}).name == "foo"
