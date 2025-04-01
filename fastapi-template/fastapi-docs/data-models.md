# Data Models

## src/fastapi_template/data_models/auth_models.py

Pydantic models for authentication.

```python
from typing import Optional, List
from pydantic import BaseModel, Field


class AccessTokenData(BaseModel):

    iss: str = Field(
        ..., description="Issuer (iss): The entity that issued the JWT token."
    )
    exp: int = Field(
        ...,
        description="Expiration Time (exp): The time when the token expires in seconds since epoch.",
    )
    nbf: int = Field(
        ...,
        description="Not Before (nbf): The time before which the token is not valid, in seconds since epoch.",
    )
    iat: int = Field(
        ...,
        description="Issued At (iat): The time when the token was issued, in seconds since epoch.",
    )
    jti: str = Field(
        ..., description="JWT ID (jti): A unique identifier for the token."
    )
    jwt_ver: int = Field(
        ..., description="JWT Version (jwt_ver): The version of the JWT format."
    )
    sub: str = Field(
        ...,
        description="Subject (sub): The subject of the token, typically a user or client ID.",
    )
    application_name: Optional[str] = Field(
        None,
        description="Application Name: Only valid when client creds generated token",
    )
    identity_type: Optional[str] = Field(
        None,
        description="Identity Type: Indicates whether this is a user account or service account.",
    )
    amr: List[str] = Field(
        ...,
        description="Authentication Methods (amr): The methods used to authenticate the user.",
    )
    auth_time: Optional[int] = Field(
        None,
        description="Authentication Time (auth_time): When the authentication occurred, in seconds since epoch.",
    )
    azp: Optional[str] = Field(
        None,
        description="Authorized Party (azp): The intended audience or client ID of the token.",
    )
    account_id: Optional[str] = Field(
        None, description="Account ID: The account or tenant identifier."
    )
    aud: List[str] = Field(
        default_factory=list,
        description="Audience (aud): The recipient(s) that the token is intended for.",
    )
    scope: Optional[str] = Field(
        None, description="Scope: The permissions granted by this token."
    )
    data_region: Optional[str] = Field(
        None,
        description="Data Region: Geographic region where the data is stored or accessed.",
    )



class UserInfoData(BaseModel):

    iss: str = Field(..., description="Issuer (iss): The entity that issued the token.")
    sub: str = Field(
        ..., description="Subject (sub): The unique identifier for the user or client."
    )
    identity_type: str = Field(
        ...,
        description="Identity Type: Indicates whether this represents a user account or service account.",
    )
    given_name: Optional[str] = Field(
        None, description="Given Name: The user's first name."
    )
    family_name: Optional[str] = Field(
        None, description="Family Name: The user's last name."
    )
    email: Optional[str] = Field(None, description="Email: The user's email address.")
    email_verified: bool = Field(
        ...,
        description="Email Verified: Indicates whether the email address has been verified.",
    )
    account_id: Optional[str] = Field(
        None,
        description="Account ID: Identifies the account or tenant associated with this token.",
    )
    locale: Optional[str] = Field(
        None,
        description="Locale: The user's language and region preferences (e.g., 'en-US').",
    )
    picture: Optional[str] = Field(
        None, description="Picture: A URL pointing to the user's profile image."
    )
    data_region: Optional[str] = Field(
        None,
        description="Data Region: Indicates the geographic region where the data is stored or accessed.",
    )
    updated_at: int = Field(
        ...,
        description="Updated At: The timestamp when this information was last updated (seconds since epoch).",
    )


class AppInfoData(BaseModel):
    service: str = Field(..., description="Application name of the service token")
    sub: str = Field(..., description="Subject (sub): Client id of the service.")


class TokenInfo(BaseModel):
    token: str
    token_data: AccessTokenData

class UserAndTokenInfo(TokenInfo):

    user_data: Optional[UserInfoData] = None
    app_data: Optional[AppInfoData] = None

    def get_email(self) -> str:
        """
        Retrieves the email address associated with the authenticated entity.

        If the authentication is for a user, returns the user's email.
        If the authentication is for an application, returns the application's service identifier.

        Returns:
            str: The email address or service identifier

        Raises:
            ValueError: If both user_data and app_data are None
        """

        if self.user_data:
            return self.user_data.email
        if self.app_data:
            return self.app_data.service
        raise ValueError("both user_data and app_data cannot be null")


```

## src/fastapi_template/data_models/__init__.py

data models package initialization.

```python
from .auth_models import TokenInfo, UserAndTokenInfo, AccessTokenData, AppInfoData, UserInfoData

```
