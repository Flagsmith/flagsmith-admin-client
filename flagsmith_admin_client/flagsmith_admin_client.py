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
        url = f"{self.api_url}/organisations/"
        response = self._make_request(url)
        return [Organisation.model_validate(org) for org in response.json()["results"]]

    def get_organisation_by_name(self, name: str) -> Organisation:
        return next(filter(lambda o: o.name == name, self.get_organisations()))

    def create_organisation(self, name: str) -> Organisation:
        data = {"name": name}
        url = f"{self.api_url}/organisations/"
        response = self._make_request(url, method="POST", data=data)
        # TODO: can we find a (pythonic) way to mutate the input object so that it
        #  includes the id. Similar to the django ORM for example.
        return Organisation.model_validate(response.json())

    def update_organisation(self, organisation: Organisation) -> Organisation:
        pass

    def delete_organisation(self, organisation: Organisation) -> None:
        url = f"{self.api_url}/organisations/{organisation.id}/"
        self._make_request(url, method="DELETE")

    def get_projects(self, organisation_id: int) -> list[Project]:
        pass

    def get_project_by_name(self, organisation_id: int, name: str) -> list[Project]:
        return next(filter(lambda p: p.name == name, self.get_projects(organisation_id)))

    def create_project(self, name: str, organisation_id: int) -> Project:
        data = {"name": name, "organisation": organisation_id}
        url = f"{self.api_url}/projects/"
        response = self._make_request(url, method="POST", data=data)
        return Project.model_validate(response.json())

    def delete_project(self, project: Project) -> None:
        pass

    def create_environment(self, name: str, project_id: int) -> Environment:
        data = {"name": name, "project": project_id}
        url = f"{self.api_url}/environments/"
        response = self._make_request(url, method="POST", data=data)
        return Environment.model_validate(response.json())

    # TODO: more environment methods

    def create_feature(self, name: str, project_id: int) -> Feature:
        data = {"name": name, "project": project_id}
        url = f"{self.api_url}/projects/{project_id}/features/"
        response = self._make_request(url, method="POST", data=data)
        return Feature.model_validate(response.json())

    # TODO: more feature methods

    def create_segment(self, name: str, project_id: int, rules: list[SegmentRule]) -> Segment:
        segment = Segment.model_validate(
            {
                "name": name,
                "project_id": project_id,
                "rules": [rule.model_dump() for rule in rules]
            }
        )
        url = f"{self.api_url}/projects/{project_id}/segments/"
        response = self._make_request(url, method="POST", data=segment.model_dump(by_alias=True))
        return Segment.model_validate(response.json())

    def _make_request(self, url: str, method: str = "GET", data: dict[str, Any] = None) -> Response:
        response: Response = getattr(self.session, method.lower())(url, json=data)
        if response.status_code >= 400:
            # TODO: better error handling
            response.raise_for_status()
        return response
