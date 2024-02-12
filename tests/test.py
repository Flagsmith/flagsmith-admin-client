import pytest

from flagsmith_admin_client.flagsmith_admin_client import FlagsmithAdminClient
from flagsmith_admin_client.models import Organisation, SegmentRule, SegmentCondition


@pytest.fixture()
def auth_token() -> str:
    return "1aa8568202cb644f6663cd091c702b1365ebc2dc"


@pytest.fixture()
def client(auth_token: str) -> FlagsmithAdminClient:
    return FlagsmithAdminClient(auth_token)


def test(client) -> None:
    organisation = Organisation(name="test from admin client")

    try:
        organisation = client.create_organisation("test from admin client")
        assert organisation.id is not None

        project = client.create_project(name="Test project", organisation_id=organisation.id)
        assert project.id

        environment = client.create_environment(name="Test environment", project_id=project.id)
        assert environment.id

        feature = client.create_feature(name="test_feature", project_id=project.id)
        assert feature.id

        client.update_flag(
            feature_id=feature.id,
            environment_key=environment.api_key,
            enabled=True,
            value="foo"
        )

        segment = client.create_segment(
            name="test segment",
            project_id=project.id,
            rules=[
                SegmentRule(
                    type="ALL",
                    rules=[
                        SegmentRule(
                            type="ALL",
                            conditions=[SegmentCondition(
                                operator="EQUAL",
                                property="foo",
                                value="bar"
                            )]
                        )
                    ]
                )
            ]
        )
        assert segment.id is not None

    finally:
        if organisation.id is not None:
            client.delete_organisation(organisation)
