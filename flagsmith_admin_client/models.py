from pydantic import BaseModel, ConfigDict, Field, AliasChoices, model_validator


class _BaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int | None = None


class Organisation(_BaseModel):
    name: str


class Project(_BaseModel):
    name: str
    organisation_id: int = Field(validation_alias=AliasChoices("organisation_id", "organisation"), serialization_alias="organisation")


class Environment(_BaseModel):
    name: str
    project_id: int = Field(validation_alias=AliasChoices("project_id", "project"), serialization_alias="project")
    api_key: str


class Feature(_BaseModel):
    name: str
    project_id: int = Field(
        validation_alias=AliasChoices("project_id", "project"),
        serialization_alias="project",
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
    project_id: int = Field(validation_alias=AliasChoices("project_id", "project"), serialization_alias="project")
    rules: list[SegmentRule] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_segment(self):
        # TODO: add validation to make sure segment looks like the ones created by the UI
        return self
