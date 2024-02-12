import typing
from typing import Any

from requests import Session, Response

from flagsmith_admin_client.models import Organisation, Project, Environment, Feature, Segment, SegmentRule

DEFAULT_API_URL = "https://api.flagsmith.com/api/v1"


class FlagsmithAdminClient:
    def __init__(self, auth_token: str, api_url: str = None):
        self.session = Session()
        self.session.headers.update(Authorization=f"Token {auth_token}")
        self.api_url = api_url or DEFAULT_API_URL

    def get_organisations(self) -> list[Organisation]:
        response = self._make_request("/organisations/")
        return [Organisation.model_validate(org) for org in response.json()["results"]]

    def get_organisation_by_name(self, name: str) -> Organisation:
        return next(filter(lambda o: o.name == name, self.get_organisations()))

    def create_organisation(self, name: str) -> Organisation:
        data = {"name": name}
        response = self._make_request("/organisations/", method="POST", json_data=data)
        # TODO: can we find a (pythonic) way to mutate the input object so that it
        #  includes the id. Similar to the django ORM for example.
        return Organisation.model_validate(response.json())

    def update_organisation(self, organisation: Organisation) -> Organisation:
        pass

    def delete_organisation(self, organisation: Organisation) -> None:
        self._make_request(f"/organisations/{organisation.id}/", method="DELETE")

    def get_projects(self, organisation_id: int) -> list[Project]:
        uri = "/projects/"
        query_params = {"organisation": str(organisation_id)}
        response = self._make_request(uri, query_params=query_params)
        return [Project.model_validate(result) for result in response.json()]

    def get_project_by_name(self, organisation_id: int, name: str) -> list[Project]:
        return next(filter(lambda p: p.name == name, self.get_projects(organisation_id)))

    def create_project(self, name: str, organisation_id: int) -> Project:
        data = {"name": name, "organisation": organisation_id}
        response = self._make_request("/projects/", method="POST", json_data=data)
        return Project.model_validate(response.json())

    def delete_project(self, project: Project) -> None:
        pass

    def create_environment(self, name: str, project_id: int) -> Environment:
        data = {"name": name, "project": project_id}
        response = self._make_request("/environments/", method="POST", json_data=data)
        return Environment.model_validate(response.json())

    def get_environments(self, project_id: int) -> list[Environment]:
        uri = "/environments/"
        query_params = {"project": str(project_id)}
        response = self._make_request(uri, query_params=query_params)
        return [Environment.model_validate(result) for result in response.json()["results"]]

    # TODO: more environment methods

    def create_feature(self, name: str, project_id: int) -> Feature:
        data = {"name": name, "project": project_id}
        response = self._make_request(f"/projects/{project_id}/features/", method="POST", json_data=data)
        return Feature.model_validate(response.json())

    # TODO: more feature methods

    def update_flag(self, feature_id: int, environment_key: str, enabled: bool, value: typing.Any) -> None:
        # get the feature state id of the feature in the environment
        response = self._make_request(
            f"/environments/{environment_key}/featurestates/",
            method="GET",
            query_params={"feature_id": str(feature_id)}
        )
        response_json = response.json()
        assert response_json["count"] == 1, "Expected 1 response, got {}".format(response_json["count"])
        feature_state_id = response_json["results"][0]["id"]

        data = {
            "enabled": enabled,
            "feature_state_value": value,
        }

        response = self._make_request(
            f"/environments/{environment_key}/featurestates/{feature_state_id}/",
            method="PATCH",
            json_data=data
        )
        assert response

    def create_segment(self, name: str, project_id: int, rules: list[SegmentRule]) -> Segment:
        segment = Segment.model_validate(
            {
                "name": name,
                "project_id": project_id,
                "rules": [rule.model_dump() for rule in rules]
            }
        )
        response = self._make_request(f"/projects/{project_id}/segments/", method="POST", json_data=segment.model_dump(by_alias=True))
        return Segment.model_validate(response.json())

    def _make_request(self, uri: str, method: str = "GET", json_data: dict[str, Any] = None, query_params: dict[str, str] = None) -> Response:
        url = f"{self.api_url}{uri}"
        if query_params:
            url += f"?{'&'.join([f'{k}={v}' for k,v in query_params.items()])}"
        response: Response = getattr(self.session, method.lower())(url, json=json_data)
        if response.status_code >= 400:
            # TODO: better error handling
            response.raise_for_status()
        return response
