# Authentication Handlers

Documentation for token-based authentication handlers.

## src/fastapi_template/tid_auth.py

Authentication handlers for token-based authentication.

```python
import logging
from typing import Optional, Dict, Union, Callable, Any, List
from fastapi import Request, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED
import httpx
import jwt
from jwt import PyJWKClient


from .data_models import UserInfoData, TokenInfo, UserAndTokenInfo, AppInfoData

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

class TidTokenAuth(OAuth2AuthorizationCodeBearer):
    """
    Handles JWT token validation using PyJWKClient.

    Parameters
    ----------
    base_url : str
        Base URL of the identity provider.
    app_name : str
        Application name or scheme.
    scopes : str, optional
        Scopes requested by the application.
    client_id : str, optional
        Client ID of the application. used for audience verification.
    auto_error : bool, optional
        Whether to raise an error if no token is provided.
    description : str, optional
        Description for the security scheme.
    verify_aud : bool, optional
        Whether to verify the audience of the token. client_id must be provided if enabled.
    extra_aud : str, optional
        extra audiences besides client_id. must be comma separated.
    jwks_client : PyJWKClient, optional
        JWKS client for JWT validation.
    """

    def __init__(
        self,
        base_url: str,
        app_name: str,
        scopes: str = None,
        client_id: str = None,
        auto_error: bool = True,
        verify_aud: bool = True,
        description: str = None,
        extra_aud: Optional[str] = None,
        jwks_client: PyJWKClient = None,
    ):
        authorization_url = f"{base_url}/oauth/authorize"
        token_url = f"{base_url}/oauth/token"
        scheme_name = app_name
        refresh_url = None
        if verify_aud and client_id is None:
            raise ValueError("client_id is required for aud verification")

        super().__init__(
            authorization_url,
            token_url,
            refresh_url,
            scheme_name,
            None, # we don't currenlty use scopes as path validators
            description,
            auto_error,
        )
        self.jwks_client: PyJWKClient = jwks_client
        self.base_url = base_url
        self.verify_aud = verify_aud
        self.client_id = client_id
        self.scopes = scopes
        self.aud : Optional[List[str]] = None
        if verify_aud:
            self.aud = [client_id]
            if extra_aud and len(extra_aud)> 0:
                extras = extra_aud.split(',')
                self.aud.extend(extras)
        logger.info('aud=%s',self.aud)


        self.app_args: Dict[str, Dict[str, Union[str, bool]]] = {
            "swagger_ui_parameters": {
                "tryItOutEnabled": True,
            },
            "swagger_ui_init_oauth": {
                "usePkceWithAuthorizationCodeGrant": True,
                "clientId": self.client_id,
                "appName": app_name,
                "scopes": self.scopes,
            },
        }


        if self.jwks_client is None:
            self.get_jwks_client()

        logger.info('tid_auth created: %s',self.app_args)

    def get_jwks_client(self):

        tid_oidc_url = f"{self.base_url}/.well-known/openid-configuration"
        logger.info("getting jwks_client from %s", tid_oidc_url)
        oidc_response = httpx.get(tid_oidc_url)
        oidc_config = oidc_response.json()
        self.jwks_client = PyJWKClient(oidc_config["jwks_uri"])
        logger.info("using jwks_uri=%s", oidc_config["jwks_uri"])

    async def __call__(self, request: Request) -> Optional[TokenInfo]:
        """
        Validates the JWT token and returns token info.

        Parameters
        ----------
        request : Request
            FastAPI request object.

        Returns
        -------
        Optional[TokenInfo]
            Parsed and validated token info, or None if not valid.
        """
        raw_token = await super().__call__(request)
        if raw_token is None:
            # is raw token is None then assume we are in auto_error=false mode and return
            return None  # pragma: nocover

        if self.jwks_client is None:
            raise HTTPException(
                HTTP_500_INTERNAL_SERVER_ERROR, detail="token validation not configured"
            )

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(raw_token)
            key = signing_key.key
            alg = signing_key._jwk_data["alg"]


            token_info = jwt.decode(
                raw_token,
                audience=self.aud,
                key=key,
                algorithms=[alg],
                require=["exp", "iat", "nbf"],
                options={"verify_aud": self.verify_aud},
            )
        except jwt.exceptions.PyJWTError as ex:
            logger.error("token error: %s", ex)
            raise HTTPException(HTTP_401_UNAUTHORIZED, detail=f"{ex}") from ex

        logger.debug("token_data=%s", token_info)
        retval = TokenInfo(token=raw_token, token_data=token_info)

        return retval

class TidUserAuth(TidTokenAuth):
    """
    Extends TidTokenAuth to additionally fetch user info from the identity provider.
    """

    def __init__(
        self,
        base_url,
        app_name,
        scopes=None,
        client_id: str = None,
        auto_error: bool = True,
        verify_aud: bool = True,
        description: str = None,
        extra_aud: Optional[str] = None,
        jwks_client: PyJWKClient = None,
    ):
        """
        Constructs a user-aware authentication object.

        Parameters
        ----------
        base_url : str
            Base URL of the identity provider.
        app_name : str
            Application name or scheme.
        scopes : str, optional
            Scopes requested by the application.
        client_id : str, optional
            Client ID of the application. used for audience verification.
        auto_error : bool, optional
            Whether to raise an error if no token is provided.
        description : str, optional
            Description for the security scheme.
        verify_aud : bool, optional
            Whether to verify the audience of the token. client_id must be provided if enabled.
        extra_aud : str, optional
            extra audiences besides client_id. must be comma separated.
        jwks_client : PyJWKClient, optional
            JWKS client for JWT validation.
        """

        super().__init__(
            base_url=base_url,
            app_name=app_name,
            scopes=scopes,
            client_id=client_id,
            auto_error=auto_error,
            verify_aud=verify_aud,
            description=description,
            extra_aud=extra_aud,
            jwks_client=jwks_client,)
        self.async_client: httpx.AsyncClient = httpx.AsyncClient()
        self.user_info_db: Dict[str, UserInfoData] = {}

    async def __call__(self, request: Request) -> Optional[UserAndTokenInfo]:
        """
        Validates token and retrieves user info if applicable.

        Parameters
        ----------
        request : Request
            FastAPI request object.

        Returns
        -------
        Optional[UserAndTokenInfo]
            Combined token and user info, or None if invalid.
        """
        token_info = await super().__call__(request)
        if token_info is None:
            return None  # pragma: nocover

        raw_retval = token_info.model_dump(exclude_none=True)

        try:
            async_client = request.app.state.async_client
        except AttributeError as ex:
            logger.error("error getting async client: %s", ex)
            async_client = self.async_client

        # sub = token_info.token_data['sub']
        sub = token_info.token_data.sub
        if token_info.token_data.identity_type == "application":
            # this is a client cred token, there is no email
            app_info = AppInfoData.model_validate({
                "service": token_info.token_data.application_name,
                "sub": token_info.token_data.sub,
            })
            raw_retval["app_data"] = app_info
            # self.user_info_db[sub] = app_info
            # self.user_info_db[sub] = {'email':token_info.token_data['application_name']}
        else:
            if sub not in self.user_info_db:
                logger.debug("getting user info for %s", sub)
                try:
                    # get the user info
                    iss = token_info.token_data.iss
                    userinfo_uri = f"{iss}/oauth/userinfo"

                    response = await async_client.get(
                        userinfo_uri,
                        headers={"Authorization": f"Bearer {token_info.token}"},
                    )

                    user_data = UserInfoData.model_validate_json(response.content)
                    logger.info("user_data = %s", user_data)
                    self.user_info_db[sub] = user_data  # deepcopy(user_data)
                except Exception as ex:
                    logger.error(
                        "error getting user info for sub=%s, error=%s", sub, ex
                    )
                    raise HTTPException(
                        HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"error getting email address. {ex}",
                    ) from ex

            raw_retval["user_data"] = self.user_info_db[sub]
        retval = UserAndTokenInfo.model_validate(raw_retval)


        return retval
```
