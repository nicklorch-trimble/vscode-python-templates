from typing import Optional, List
from pydantic import BaseModel, Field


class AccessTokenData(BaseModel):
    """
    AccessTokenData represents the structure of an access token with various claims.

    Attributes:
        iss (str): Issuer (iss): The entity that issued the JWT token.
        exp (int): Expiration Time (exp): The time when the token expires in seconds since epoch.
        nbf (int): Not Before (nbf): The time before which the token is not valid, in seconds since epoch.
        iat (int): Issued At (iat): The time when the token was issued, in seconds since epoch.
        jti (str): JWT ID (jti): A unique identifier for the token.
        jwt_ver (int): JWT Version (jwt_ver): The version of the JWT format.
        sub (str): Subject (sub): The subject of the token, typically a user or client ID.
        application_name (Optional[str]): Application Name: Only valid when client creds generated token.
        identity_type (Optional[str]): Identity Type: Indicates whether this is a user account or service account.
        amr (List[str]): Authentication Methods (amr): The methods used to authenticate the user.
        auth_time (Optional[int]): Authentication Time (auth_time): When the authentication occurred, in seconds since epoch.
        azp (Optional[str]): Authorized Party (azp): The intended audience or client ID of the token.
        account_id (Optional[str]): Account ID: The account or tenant identifier.
        aud (List[str]): Audience (aud): The recipient(s) that the token is intended for.
        scope (Optional[str]): Scope: The permissions granted by this token.
        data_region (Optional[str]): Data Region: Geographic region where the data is stored or accessed.
    """

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
    """
    A pydantic model that represents the user information extracted from a token.

    This model contains fields that are typically found in OpenID Connect ID tokens,
    along with some Trimble-specific fields. It represents a user's identity and
    profile information that can be used for authentication and authorization purposes.

    Attributes:
        iss (str): Issuer identifier for the token.
        sub (str): Subject identifier for the user or client.
        identity_type (str): Identifies whether this is a user account or service account.
        given_name (Optional[str]): The user's first name, if available.
        family_name (Optional[str]): The user's last name, if available.
        email (Optional[str]): The user's email address, if available.
        email_verified (bool): Whether the user's email has been verified.
        account_id (Optional[str]): The identifier for the account/tenant associated with this token.
        locale (Optional[str]): The user's language and region preferences (e.g., 'en-US').
        picture (Optional[str]): URL to the user's profile image, if available.
        data_region (Optional[str]): Geographic region associated with the user's data.
        updated_at (int): Unix timestamp (seconds since epoch) when the information was last updated.
    """

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
    """
    A class representing application information data.

    This class models the data extracted from a service token's claims or similar authentication context.

    Attributes:
        service (str): Application name of the service token.
        sub (str): Subject (sub): Client id of the service.
    """

    service: str = Field(..., description="Application name of the service token")
    sub: str = Field(..., description="Subject (sub): Client id of the service.")


class TokenInfo(BaseModel):
    """
    Wraps a raw token and its decoded information.

    Attributes
    ----------
    token : str
        The raw JWT string.
    token_data : AccessTokenData
        Decoded JWT payload.
    """

    token: str
    token_data: AccessTokenData

class UserAndTokenInfo(TokenInfo):
    """
    Combines token information with user or application data.

    Attributes
    ----------
    user_data : Optional[UserInfoData]
        User-specific data if a user token.
    app_data : Optional[AppInfoData]
        Application-specific data if a service token.
    """

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

