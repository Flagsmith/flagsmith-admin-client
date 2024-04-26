import csv
import os
import sys
from datetime import datetime

from flagsmith_admin_client.flagsmith_admin_client import FlagsmithAdminClient
from flagsmith_admin_client.models import Feature


def format_date(date: datetime):
    return date.strftime("%d %b %Y %X") if date else None


excluded_fields = [
    "environment_state",
    "multivariate_options",
    "initial_value",
    "tags",
    "project_id",
    "id",
]

client = FlagsmithAdminClient(os.environ.get("FLAGSMITH_TOKEN"))
organisation = client.get_organisation_by_name("Flagsmith")

properties = Feature.model_json_schema()["properties"]
for f in excluded_fields:
    del properties[f]
fieldnames = ["project", "environment", "enabled", *list(properties)]

filename_date = datetime.now().isoformat(timespec="seconds")
filename = f"Flagsmith features - {organisation.name} - {filename_date}.csv"
with open(filename, "w", encoding="utf-8") as file:
    print(f'Saving features to "{filename}"...', file=sys.stderr)
    writer = csv.DictWriter(file, fieldnames)
    writer.writeheader()
    projects = client.get_projects(organisation.id)
    features_saved = 0
    for p in projects:
        environments = client.get_environments(project_id=p.id)
        for e in environments:
            for f in client.get_features(
                environment_id=e.id, project_id=p.id, page_size=1000
            ):
                features_saved += 1
                dict = f.model_dump(exclude=excluded_fields)
                # Avoids writing actual feature value in case it's sensitive
                dict["enabled"] = f.environment_state.enabled
                dict["created_date"] = format_date(f.created_date)
                dict["environment"] = e.name
                dict["project"] = p.name
                dict["last_modified_in_any_environment"] = format_date(
                    f.last_modified_in_any_environment
                )
                dict["last_modified_in_current_environment"] = format_date(
                    f.last_modified_in_current_environment
                )
                writer.writerow(dict)
    print(f"Saved {features_saved} features")
