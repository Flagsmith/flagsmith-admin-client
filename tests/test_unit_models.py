from flagsmith_admin_client.models import Feature


def test_feature() -> None:
    assert Feature.model_validate({"id": 1, "name": "foo"}).name == "foo"

def test_standard_feature() -> None:
    standard_feature = """
    {
      "id": 91052,
      "name": "landing.welcome_message",
      "type": "STANDARD",
      "default_enabled": false,
      "initial_value": "Welcome!",
      "created_date": "2024-04-17T18:25:28.232655Z",
      "description": null,
      "tags": [
        9589
      ],
      "multivariate_options": [],
      "is_archived": false,
      "owners": [
        {
          "id": 21845,
          "email": "rodrigo.lopezdato@flagsmith.com",
          "first_name": "Rodrigo",
          "last_name": "López Dato",
          "last_login": "2024-04-24T18:23:17.648774Z"
        }
      ],
      "group_owners": [],
      "uuid": "e1459f3a-3669-48e8-8f8d-a096d89f578e",
      "project": 16945,
      "environment_feature_state": {
        "id": 515958,
        "feature_state_value": "Welcome!",
        "environment": 44250,
        "identity": null,
        "feature_segment": null,
        "enabled": false
      },
      "num_segment_overrides": 0,
      "num_identity_overrides": 1,
      "is_server_key_only": false,
      "last_modified_in_any_environment": "2024-04-23T16:22:36.900034+00:00",
      "last_modified_in_current_environment": null
    }
    """
    assert Feature.model_validate_json(standard_feature)

def test_multivariate_feature() -> None:
    multivariate_feature = """
    {
        "id": 91319,
        "name": "landing.background_colour",
        "type": "MULTIVARIATE",
        "default_enabled": false,
        "initial_value": "blue",
        "created_date": "2024-04-19T13:17:34.103652Z",
        "description": null,
        "tags": [],
        "multivariate_options": [
            {
            "id": 12362,
            "uuid": "14578d41-501f-4473-92f5-c1dfd9d63464",
            "type": "unicode",
            "integer_value": null,
            "string_value": "green",
            "boolean_value": null,
            "default_percentage_allocation": 0.0
            },
            {
            "id": 12361,
            "uuid": "eb63e35a-303e-4676-9333-b72ca49351e4",
            "type": "unicode",
            "integer_value": null,
            "string_value": "orange",
            "boolean_value": null,
            "default_percentage_allocation": 0.0
            }
        ],
        "is_archived": false,
        "owners": [
            {
            "id": 21845,
            "email": "rodrigo.lopezdato@flagsmith.com",
            "first_name": "Rodrigo",
            "last_name": "López Dato",
            "last_login": "2024-04-24T18:23:17.648774Z"
            }
        ],
        "group_owners": [],
        "uuid": "f13e4238-5fbd-4b2c-b222-7c534a5f16d6",
        "project": 16945,
        "environment_feature_state": {
            "id": 516928,
            "feature_state_value": "blue",
            "environment": 44250,
            "identity": null,
            "feature_segment": null,
            "enabled": false
        },
        "num_segment_overrides": 1,
        "num_identity_overrides": null,
        "is_server_key_only": false,
        "last_modified_in_any_environment": "2024-04-23T16:22:36.994159+00:00",
        "last_modified_in_current_environment": null
    }
    """
    assert Feature.model_validate_json(multivariate_feature)