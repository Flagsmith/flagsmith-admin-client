import pytest

from flagsmith_admin_client.flagsmith_admin_client import FlagsmithAdminClient
from flagsmith_admin_client.models import Organisation, Project, Environment, Feature, Segment, SegmentRule, \
    SegmentCondition


@pytest.fixture()
def auth_token() -> str:
    return ""


@pytest.fixture()
def client(auth_token: str) -> FlagsmithAdminClient:
    return FlagsmithAdminClient(auth_token)


def test(client) -> None:
    organisation = Organisation(name="test from admin client")

    try:
        organisation = client.create_organisation(organisation)
        assert organisation.id is not None

        project = client.create_project(Project(name="Test project", organisation_id=organisation.id))
        assert project.id

        environment = client.create_environment(Environment(name="Test environment", project_id=project.id))
        assert environment.id

        feature = client.create_feature(Feature(name="test_feature", project_id=project.id))
        assert feature.id

        segment = Segment(
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
        segment = client.create_segment(segment)
        assert segment.id is not None

    finally:
        if organisation.id is not None:
            client.delete_organisation(organisation)
