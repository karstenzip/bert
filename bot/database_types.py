from __future__ import annotations

import datetime
import uuid
from typing import (
    Annotated,
    Any,
    List,
    Literal,
    Optional,
    TypedDict,
)
from typing_extensions import NotRequired, TypeAlias

from pydantic import BaseModel, Field, JsonValue

AuthAalLevel: TypeAlias = Literal["aal1", "aal2", "aal3"]

AuthCodeChallengeMethod: TypeAlias = Literal["s256", "plain"]

AuthFactorStatus: TypeAlias = Literal["unverified", "verified"]

AuthFactorType: TypeAlias = Literal["totp", "webauthn", "phone", "recovery_code"]

AuthOauthAuthorizationStatus: TypeAlias = Literal["pending", "approved", "denied", "expired"]

AuthOauthClientType: TypeAlias = Literal["public", "confidential"]

AuthOauthRegistrationType: TypeAlias = Literal["dynamic", "manual"]

AuthOauthResponseType: TypeAlias = Literal["code"]

AuthOneTimeTokenType: TypeAlias = Literal["confirmation_token", "reauthentication_token", "recovery_token", "email_change_token_new", "email_change_token_current", "phone_change_token"]

RealtimeAction: TypeAlias = Literal["INSERT", "UPDATE", "DELETE", "TRUNCATE", "ERROR"]

RealtimeEqualityOp: TypeAlias = Literal["eq", "neq", "lt", "lte", "gt", "gte", "in", "like", "ilike", "is", "match", "imatch", "isdistinct"]

StorageBuckettype: TypeAlias = Literal["STANDARD", "ANALYTICS", "VECTOR"]

class PublicStats(BaseModel):
    guild_id: str = Field(alias="guild_id")
    name: str = Field(alias="name")
    user_id: str = Field(alias="user_id")
    value: int = Field(alias="value")

class PublicStatsInsert(TypedDict):
    guild_id: Annotated[str, Field(alias="guild_id")]
    name: Annotated[str, Field(alias="name")]
    user_id: Annotated[str, Field(alias="user_id")]
    value: NotRequired[Annotated[int, Field(alias="value")]]

class PublicStatsUpdate(TypedDict):
    guild_id: NotRequired[Annotated[str, Field(alias="guild_id")]]
    name: NotRequired[Annotated[str, Field(alias="name")]]
    user_id: NotRequired[Annotated[str, Field(alias="user_id")]]
    value: NotRequired[Annotated[int, Field(alias="value")]]

class PublicVcmaker(BaseModel):
    channel: str = Field(alias="channel")
    owner: Optional[str] = Field(alias="owner")
    permanent: bool = Field(alias="permanent")

class PublicVcmakerInsert(TypedDict):
    channel: Annotated[str, Field(alias="channel")]
    owner: NotRequired[Annotated[Optional[str], Field(alias="owner")]]
    permanent: Annotated[bool, Field(alias="permanent")]

class PublicVcmakerUpdate(TypedDict):
    channel: NotRequired[Annotated[str, Field(alias="channel")]]
    owner: NotRequired[Annotated[Optional[str], Field(alias="owner")]]
    permanent: NotRequired[Annotated[bool, Field(alias="permanent")]]
