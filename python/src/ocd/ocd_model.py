import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, ValidationError, field_validator


UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
SLUG_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")


class LocalizedText(BaseModel):
    text: str
    lang: str

    model_config = dict(extra="forbid")


class Names(BaseModel):
    canon: str
    display: Optional[Union[List[LocalizedText], Dict[str, str]]] = None
    aliases: Optional[List[str]] = None
    epithets: Optional[List[str]] = None

    model_config = dict(extra="allow")

    @field_validator("canon")
    @classmethod
    def non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("canon must be a non-empty string")
        return value


class Measurement(BaseModel):
    value: float
    unit: str

    model_config = dict(extra="forbid")


class AgeBlock(BaseModel):
    nominal: Optional[Measurement] = None
    biological: Optional[Measurement] = None
    chronological: Optional[Measurement] = None
    chrono_override: Optional[Measurement] = None
    rationale: Optional[str] = None

    model_config = dict(extra="forbid")


class Origins(BaseModel):
    universe: Optional[str] = None
    birthplace: Optional[str] = None
    debut_date: Optional[str] = None

    model_config = dict(extra="forbid")

    @field_validator("debut_date")
    @classmethod
    def valid_date(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        datetime.strptime(value, "%Y-%m-%d")
        return value


class Continuity(BaseModel):
    canon: Optional[Literal["prime", "alt", "fanon", "apocrypha"]] = None
    timeline_ids: Optional[List[str]] = None

    model_config = dict(extra="forbid")


class CompositeMember(BaseModel):
    ref: str
    control_share: float = Field(ge=0.0, le=1.0)
    exposure: Literal["public", "secret"]
    visibility: Optional[str] = None

    model_config = dict(extra="allow")

    @field_validator("ref")
    @classmethod
    def valid_uuid(cls, value: str) -> str:
        if not UUID_RE.match(value):
            raise ValueError("ref must be a uuid")
        return value


class SecretIdentity(BaseModel):
    public_name: str
    exposure_risk: float = Field(ge=0.0, le=1.0)

    model_config = dict(extra="allow")


class Identity(BaseModel):
    entity_kind: Literal["person", "collective", "creature", "object", "place", "abstract", "ai"]
    sapience_level: Literal["animal", "tool", "agent", "sapient", "transcendent"]
    species: Optional[Literal["human", "ai", "alien", "collective", "object", "deity", "other"]] = None
    pronouns: Optional[List[str]] = None
    age: Optional[AgeBlock] = None
    origins: Optional[Origins] = None
    continuity: Optional[Continuity] = None
    roles: Optional[List[Literal["protagonist", "antagonist", "support", "ensemble", "npc", "avatar"]]] = None
    composite_of: Optional[List[CompositeMember]] = None
    secret_identities: Optional[List[SecretIdentity]] = None

    model_config = dict(extra="allow")


class Versioning(BaseModel):
    created_at: str
    last_modified: str
    change_log: Optional[List[str]] = None

    model_config = dict(extra="allow")

    @field_validator("created_at", "last_modified")
    @classmethod
    def iso8601(cls, value: str) -> str:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class Creator(BaseModel):
    name: str
    role: Optional[str] = None

    model_config = dict(extra="allow")


class Rights(BaseModel):
    owner: Optional[str] = None
    license: Optional[str] = None
    usage_notes: Optional[str] = None

    model_config = dict(extra="allow")


class AuditTrail(BaseModel):
    edited_by: Optional[str] = None
    source_files: Optional[List[str]] = None

    model_config = dict(extra="allow")


class Meta(BaseModel):
    versioning: Versioning
    creators: Optional[List[Creator]] = None
    rights: Optional[Rights] = None
    external_ids: Optional[Dict[str, str]] = None
    tags: Optional[List[str]] = None
    audit: Optional[AuditTrail] = None

    model_config = dict(extra="allow")


class ScaleRange(BaseModel):
    min: float = 0.0
    max: float = 1.0

    model_config = dict(extra="forbid")


class BipolarTrait(BaseModel):
    kind: Literal["bipolar"]
    key: str
    value: float = Field(ge=-1.0, le=1.0)
    id: Optional[str] = None
    label: Optional[str] = None
    poles: Optional[List[str]] = None

    model_config = dict(extra="allow")


class ScalarTrait(BaseModel):
    kind: Literal["scalar"]
    key: str
    value: float
    scale: Optional[ScaleRange] = None
    id: Optional[str] = None
    label: Optional[str] = None

    model_config = dict(extra="allow")

    @classmethod
    def model_validate(cls, data: Any) -> "ScalarTrait":  # type: ignore[override]
        obj = super().model_validate(data)
        scale = obj.scale or ScaleRange()
        min_val = scale.min
        max_val = scale.max
        if obj.value < min_val or obj.value > max_val:
            raise ValidationError.from_exception_data(
                cls.__name__,
                [
                    {
                        "loc": ("value",),
                        "msg": f"{cls.__name__}.value {obj.value} outside [{min_val}, {max_val}]",
                        "type": "value_error",
                        "input": obj.value,
                        "ctx": {
                            "model": cls.__name__,
                            "min": min_val,
                            "max": max_val,
                        },
                    }
                ],
            )
        return obj


class CategoricalTrait(BaseModel):
    kind: Literal["categorical"]
    key: str
    value: str
    options: Optional[List[str]] = None
    id: Optional[str] = None
    label: Optional[str] = None

    model_config = dict(extra="allow")


class FlagTrait(BaseModel):
    kind: Literal["flag"]
    key: str
    value: bool
    id: Optional[str] = None
    label: Optional[str] = None

    model_config = dict(extra="allow")


class ProfileTrait(BaseModel):
    kind: Literal["profile"]
    key: str
    facets: Dict[str, float]
    id: Optional[str] = None
    label: Optional[str] = None

    model_config = dict(extra="allow")


Trait = Union[BipolarTrait, ScalarTrait, CategoricalTrait, FlagTrait, ProfileTrait]


class Personality(BaseModel):
    traits: Optional[List[Trait]] = None
    motivations: Optional[List[Dict[str, Any]]] = None
    speech: Optional[Dict[str, Any]] = None

    model_config = dict(extra="allow")


class PhysicalDescriptor(BaseModel):
    height: Optional[Measurement] = None
    weight: Optional[Measurement] = None
    descriptors: Optional[List[str]] = None
    build: Optional[str] = None
    color_palette: Optional[List[Dict[str, Any]]] = None

    model_config = dict(extra="allow")


class Portrait(BaseModel):
    uri: str
    credit: Optional[str] = None
    media: Optional[str] = None

    model_config = dict(extra="allow")


class Outfit(BaseModel):
    id: str
    name: str
    descriptors: Optional[List[str]] = None

    model_config = dict(extra="allow")

    @field_validator("id")
    @classmethod
    def valid_uuid(cls, value: str) -> str:
        if not UUID_RE.match(value):
            raise ValueError("id must be a uuid")
        return value


class FormDelta(BaseModel):
    id: str
    name: str
    delta_from_baseline: Optional[Dict[str, Any]] = None
    triggers: Optional[List[str]] = None

    model_config = dict(extra="allow")

    @field_validator("id")
    @classmethod
    def valid_uuid(cls, value: str) -> str:
        if not UUID_RE.match(value):
            raise ValueError("id must be a uuid")
        return value


class Appearance(BaseModel):
    baseline: Optional[PhysicalDescriptor] = None
    portraits: Optional[List[Portrait]] = None
    outfits: Optional[List[Outfit]] = None
    forms: Optional[List[FormDelta]] = None
    art_style: Optional[str] = None

    model_config = dict(extra="allow")


class Ability(BaseModel):
    id: Optional[str] = None
    name: str
    kind: Optional[str] = None
    cost: Optional[Dict[str, Any]] = None
    effects: Optional[List[Dict[str, Any]]] = None
    cooldown: Optional[Measurement] = None
    prerequisites: Optional[List[str]] = None
    counters: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    model_config = dict(extra="allow")


class Metaphysics(BaseModel):
    power_system: Optional[Dict[str, Any]] = None
    abilities: Optional[List[Ability]] = None
    constraints: Optional[List[str]] = None
    vulnerabilities: Optional[List[Dict[str, Any]]] = None
    resistances: Optional[List[Dict[str, Any]]] = None

    model_config = dict(extra="allow")


class Background(BaseModel):
    biography: Optional[List[Dict[str, Any]]] = None
    affiliations: Optional[List[Dict[str, Any]]] = None
    relationships: Optional[List[Dict[str, Any]]] = None
    milestones: Optional[List[Dict[str, Any]]] = None

    model_config = dict(extra="allow")


class Behavior(BaseModel):
    action_repertoire: Optional[List[str]] = None
    combat_style: Optional[Dict[str, Any]] = None
    ai: Optional[Dict[str, Any]] = None

    model_config = dict(extra="allow")


class MediaProfiles(BaseModel):
    game_rpg: Optional[Dict[str, Any]] = None
    fighting: Optional[Dict[str, Any]] = None
    visual_novel: Optional[Dict[str, Any]] = None
    theater: Optional[Dict[str, Any]] = None
    film_tv: Optional[Dict[str, Any]] = None
    comics: Optional[Dict[str, Any]] = None

    model_config = dict(extra="allow")


class CharacterDefinition(BaseModel):
    kind: Literal["CharacterDefinition"]
    ocd_version: str
    id: str
    slug: str
    names: Names
    identity: Identity
    meta: Meta
    appearance: Optional[Appearance] = None
    metaphysics: Optional[Metaphysics] = None
    personality: Optional[Personality] = None
    background: Optional[Background] = None
    behavior: Optional[Behavior] = None
    media_profiles: Optional[MediaProfiles] = None
    extras: Optional[Dict[str, Any]] = None

    model_config = dict(extra="allow")

    @field_validator("id")
    @classmethod
    def valid_uuid(cls, value: str) -> str:
        try:
            uuid.UUID(value)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("id must be a uuid") from exc
        return value

    @field_validator("slug")
    @classmethod
    def valid_slug(cls, value: str) -> str:
        if not SLUG_RE.match(value):
            raise ValueError("slug must match ^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
        return value


class Stat(BaseModel):
    key: str
    value: Union[int, float, str, Dict[str, Any], List[Any], bool]
    unit: Optional[str] = None
    min: Optional[float] = None
    max: Optional[float] = None
    temp: Optional[bool] = None

    model_config = dict(extra="allow")


class EffectTimer(BaseModel):
    value: float = Field(ge=0.0)
    unit: str

    model_config = dict(extra="forbid")


class ActiveEffect(BaseModel):
    effect: str
    remaining: Optional[EffectTimer] = None
    source_ref: Optional[str] = None

    model_config = dict(extra="allow")


class Cooldown(BaseModel):
    ability_ref: str
    remaining: EffectTimer

    model_config = dict(extra="allow")


class InstanceState(BaseModel):
    stats: Optional[List[Stat]] = None
    location_ref: Optional[str] = None
    active_effects: Optional[List[ActiveEffect]] = None
    cooldowns: Optional[List[Cooldown]] = None

    model_config = dict(extra="allow")


class CharacterInstance(BaseModel):
    kind: Literal["CharacterInstance"]
    ocd_version: str
    instance_id: str
    from_def: str
    state: InstanceState
    progression: Optional[Dict[str, Any]] = None
    session: Optional[Dict[str, Any]] = None
    extras: Optional[Dict[str, Any]] = None

    model_config = dict(extra="allow")

    @field_validator("instance_id", "from_def")
    @classmethod
    def valid_uuid(cls, value: str) -> str:
        if not UUID_RE.match(value):
            raise ValueError("must be a uuid")
        return value
