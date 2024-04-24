from datetime import date, datetime, time, timedelta
from typing import Any, List, Optional

from pydantic import (AliasChoices, BaseModel, ConfigDict, Field, SerializeAsAny,
                      model_validator)


class _BaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int | None = None


class Organisation(_BaseModel):
    name: str


class Project(_BaseModel):
    name: str
    organisation_id: int = Field(
        validation_alias=AliasChoices("organisation_id", "organisation"),
        serialization_alias="organisation",
    )


class Environment(_BaseModel):
    name: str
    project_id: int = Field(
        validation_alias=AliasChoices("project_id", "project"),
        serialization_alias="project",
    )
    api_key: str


class Feature(_BaseModel):
    class FeatureState(BaseModel):
        environment_id: int = Field(
            validation_alias=AliasChoices("environment_id", "environment"),
            serialization_alias="environment"
        )
        enabled: bool
        value: Optional[str | int | float] = Field(
            validation_alias=AliasChoices("value", "feature_state_value"),
            serialization_alias="feature_state_value",
            default=None,
        )
    class MultivariateOption(BaseModel):
        integer_value: Optional[int]
        string_value: Optional[str]
        boolean_value: Optional[bool]
        default_percentage_allocation: float
        

    name: str
    type: Optional[str] = None
    default_enabled: Optional[bool] = None
    initial_value: Optional[str | int | float] = None
    created_date: Optional[datetime] = None
    description: Optional[str] = None
    tags: List[int] = []
    multivariate_options: List[MultivariateOption] = []
    is_archived: bool = False
    project_id: int = Field(
        validation_alias=AliasChoices("project_id", "project"),
        serialization_alias="project",
        default=None,
    )
    num_segment_overrides: Optional[int] = 0
    num_identity_overrides: Optional[int] = 0
    is_server_key_only: bool = False
    last_modified_in_any_environment: Optional[datetime] = None
    last_modified_in_current_environment: Optional[datetime] = None
    environment_state: Optional[FeatureState] = Field(
        validation_alias=AliasChoices("environment_state", "environment_feature_state"),
        serialization_alias="environment_feature_state",
        default=None
    )


class SegmentCondition(_BaseModel):
    operator: str
    property: str | None = None
    value: str | None = None


class SegmentRule(_BaseModel):
    type: str = Field()
    rules: list["SegmentRule"] = Field(default_factory=list)
    conditions: list[SegmentCondition] = Field(default_factory=list)


class Segment(_BaseModel):
    name: str
    project_id: int = Field(
        validation_alias=AliasChoices("project_id", "project"),
        serialization_alias="project",
    )
    rules: list[SegmentRule] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_segment(self):
        # TODO: add validation to make sure segment looks like the ones created by the UI
        return self
