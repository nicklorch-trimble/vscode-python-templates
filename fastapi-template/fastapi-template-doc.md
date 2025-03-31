# FastAPI Project Template Documentation

This document describes the structure and components of the FastAPI template project. This template follows best practices for creating FastAPI applications with proper structure, authentication, environment configuration, and development tools.

## Project Structure

```
fastapi-template/
├── .vscode/                    # VS Code configuration
│   ├── launch.json             # Debug configurations
│   └── settings.json           # Editor settings
├── src/                        # Source code
│   └── fastapi_template/       # Main package
│       ├── data_models/        # Pydantic models
│       │   ├── __init__.py
│       │   └── auth_models.py  # Authentication models
│       ├── routers/            # API route definitions
│       │   ├── __init__.py
│       │   └── api.py          # API endpoints
│       ├── __init__.py         # Package initialization
│       ├── create_app.py       # Application factory
│       ├── dev.py              # Development utilities
│       ├── gen_env_template.py # Environment template generator
│       ├── main.py             # Application entry point
│       ├── settings.py         # Configuration settings
│       └── tid_auth.py         # Authentication handlers
├── .bumpversion.toml           # Version management configuration
└── pyproject.toml              # Project dependencies and metadata
```

## File Contents

### pyproject.toml

This file defines the project metadata, dependencies, development tools, and build system.

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fastapi-template"
version = "0.0.1"
dependencies = [
	"fastapi[all]",
  "pydantic_settings",
	"coloredlogs",
  'pyjwt[crypto]',
]
requires-python = ">=3.10"
authors = [
  { name = "Nick Lorch", email = "nick_lorch@trimble.com" },
]
maintainers = [
  { name = "Nick Lorch", email = "nick_lorch@trimble.com" },
]
description = "FastAPI template"
readme = "README.md"
classifiers = [
    "Programming Language :: Python :: 3.10",
    "Typing :: Typed",
]

[project.optional-dependencies]
dev = [
    'bump-my-version',
    'build',
    'wheel',
]

[project.urls]
Homepage = "https://github.com/nicklorch-trimble/vscode-python-templates/fastapi-template"
Documentation = "https://github.com/nicklorch-trimble/vscode-python-templates/fastapi-template"
Repository = "https://github.comnicklorch-trimble/fastapi-template/vscode-python-templates.git"

[project.entry-points.console_scripts]
    "fastapi-template" = "fastapi_template.main:main"
    "gen-env" = "fastapi_template.gen_env_template:main"

```

### .bumpversion.toml

This file configures version bumping for the project.

```toml
[tool.bumpversion]
current_version = "0.0.1"
commit = true
commit_args = "--no-verify"
tag = true
tag_name = "v{new_version}"
allow_dirty = true
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\.(?P<dev>post)\\d+\\.dev\\d+)?"
serialize = [
    "{major}.{minor}.{patch}.{dev}.dev{distance_to_latest_tag}",
    "{major}.{minor}.{patch}"
]
message = "Version updated from {current_version} to {new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = "version = \"{current_version}\""
replace = "version = \"{new_version}\""
```

### .vscode/launch.json

VS Code debug configurations for the project.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastApiServer",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/venv/bin/fastapi-template",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### .vscode/settings.json

VS Code editor settings for the project.

```json
{
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.terminal.activateEnvironment": true,
    "python.autoComplete.extraPaths": [
        ".",
        "${workspaceFolder}",
        "${workspaceFolder}/src"
    ],
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "python.linting.ignorePatterns": [
        ".vscode/*.py",
        "**/site-packages/**/*.py",
        "tmp/*.py"
    ],
    "python.formatting.provider": "yapf",
    "python.formatting.autopep8Args": ["--max-line-length","120"],
    "python.formatting.yapfArgs": ["--style","{based_on_style: facebook}"],
    "python.linting.pylintCategorySeverity.refactor": "Information",
    "python.analysis.extraPaths": [
        ".",
        "${workspaceFolder}",
        "${workspaceFolder}/src"
    ],
    "python.testing.pytestArgs": [],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/.hg/store/**": true
    },
    "[python]": {
        "editor.formatOnType": false
    }
}
```

### src/fastapi_template/create_app.py

Factory function to create and configure the FastAPI application.

```python
import logging
from contextlib import asynccontextmanager
from typing import Annotated
from pydantic import BaseModel
from fastapi.routing import APIRoute
from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN
import coloredlogs
import httpx

from . import get_my_package_name,get_my_package_version, get_settings, get_tid_auth
from .data_models import TokenInfo,UserAndTokenInfo, AccessTokenData

from .routers import ROUTER_LIST


logger = logging.getLogger(__name__)
logger.setLevel('INFO')

coloredlogs.install()



def custom_generate_unique_id(route: APIRoute) -> str:
    """This function generates friendly names when the swagger document is used for code generation. """
    return f"{route.name}"


def create_app() -> FastAPI:
    """Creates FASTAPI application

    Returns
    -------
    FastAPI
        newly created api
    """

    settings = get_settings()
    tid = get_tid_auth()

    @asynccontextmanager
    async def lifespan(app: FastAPI):

        async with httpx.AsyncClient() as async_client:

            # everything before the yield is app startup functionality
            app.state.async_client = async_client

            # put the dummy db manager in the state so we can access it in the route methods

            yield
            # everything after the yield is app shutdown functionality
            app.state.async_client = None
            print('cleanup complete')


    app_args = {
        'version':get_my_package_version(),
        'title':get_my_package_name(),
        'lifespan':lifespan,
        'generate_unique_id_function':custom_generate_unique_id,
        **tid.app_args
    }

    app = FastAPI(**app_args)

    # setup CORS
    origins = [
        'http://localhost',
        'http://localhost:8000',
        'http://localhost:8888',
        'http://0.0.0.0',
        'http://0.0.0.0:8000',
        'http://0.0.0.0:8888',
    ]

    if settings.cors_extra_origins is not None and len(settings.cors_extra_origins) > 0:
        extra_origins = [origin.strip() for origin in settings.cors_extra_origins.split(',') if 'http' in origin]
        if len(extra_origins) > 0:
            logger.info('adding extra origins: %s', extra_origins)
            origins.extend(extra_origins)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    for router in ROUTER_LIST:
        app.include_router(router)

    # dummy route to test the app
    @app.get('/', include_in_schema=False)
    async def hello_world(request:Request):
        return {"hello":"world"}

    return app

```

### src/fastapi_template/data_models/auth_models.py

Pydantic models for authentication.

```python
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


```

### src/fastapi_template/data_models/__init__.py

data models package initialization.

```python
from .auth_models import TokenInfo, UserAndTokenInfo, AccessTokenData, AppInfoData, UserInfoData

```

### src/fastapi_template/routers/api.py

API route definitions.

```python
from fastapi import APIRouter, Depends, HTTPException, Request, Depends
from typing import List, Annotated
from pydantic import BaseModel

from .. import get_my_package_name,get_my_package_version,get_tid_auth
from ..data_models import UserAndTokenInfo


api_router = APIRouter(
    tags=["Users"],
    prefix="/api",

)

class VersionResponse(BaseModel):
    api_name:str
    api_version:str


@api_router.get('/health')
async def health_endpoint(request:Request):
    # add some health checks here
    return {"status":"great"}

# put in a call for the api version
@api_router.get("/version")
async def get_api_version() -> VersionResponse:
    return VersionResponse(api_name=get_my_package_name(),api_version=get_my_package_version())

@api_router.get('/token_info',response_model_exclude_none=True)
async def get_token_info(token_info:Annotated[UserAndTokenInfo,Depends(get_tid_auth())])->UserAndTokenInfo:
    """Validates the following:
    * Authorization Header is present
    * jwt is a valid jwt and signature is correct.
    * audience matches provided allowed audiences
    * user profile or app name depending on the token
    """
    return token_info

```

### src/fastapi_template/routers/__init__.py

Router package initialization.

```python
from .api import api_router

# convienence method to get all routers
ROUTER_LIST = [api_router]

```

### src/fastapi_template/settings.py

Application settings using Pydantic settings management.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    tid_client_name:str = "fastapi-template"
    tid_client_id:str = "unique client id"
    tid_scopes:str = "openid fastapi-template"
    tid_base_url:str = "https://identityurl.com"
    tid_oidc_url:str = "https://identityurl.com/.well-known/openid-configuration"

    cors_extra_origins:str = ''

    model_config = SettingsConfigDict(
        env_prefix='fastapi_template_',  # Prefix for environment variables
        env_file=(".env", ".env.dev", ".env.prod")
    )


```

### src/fastapi_template/main.py

Application entry point.

```python
from pathlib import Path
import logging
import logging.config
import json
import argparse
import uvicorn
import coloredlogs
from .create_app import create_app, get_my_package_name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',default='0.0.0.0')
    parser.add_argument('-p','--port',default=8000,type=int)
    parser.add_argument('-q','--quiet',action='store_true')
    parser.add_argument('-r','--reload',action='store_true', help='enable hot reloading')
    parser.add_argument('--gen-openapi',action='store_true', help='generate openapi schema and then quit')
    parser.add_argument('-o','--gen-openapi-path',default=f'{get_my_package_name()}-openapi.json', help='path to save openapi schema')
    args = parser.parse_args()

    # Configure logging
    if args.quiet:
        print('running in quiet mode')
        logging.basicConfig(level='ERROR')
        coloredlogs.install(level='ERROR')
    else:
        # Default to basic config if no config file found
        logging.basicConfig(level='INFO')
        coloredlogs.install(level='INFO')
        logging.info("Using default logging configuration")

    uvicorn_logger = logging.getLogger('uvicorn.access')
    uvicorn_logger.disabled = True

    startup_args = {
        'host': args.host,
        'port': args.port,
        'proxy_headers': True,
        'reload': args.reload
    }

    if args.reload:
        # for hot reloading we have to use a string to the app
        app = f"{get_my_package_name().replace('-','_')}.dev:dev_app"
    else:
        # for runtime we can use the actual app object
        app = create_app()
        if args.gen_openapi:
            logging.info('creating openapi schema')
            openapi_schema = app.openapi()
            openapi_path = Path(args.gen_openapi_path)
            with open(openapi_path,'w', encoding="UTF-8") as f:
                json.dump(openapi_schema,f,indent=2)
            logging.info('OpenAPI schema saved to %s',openapi_path.absolute())
            return

    uvicorn.run(app, **startup_args)

if __name__ == "__main__":
    main()

```

### src/fastapi_template/__init__.py

Common utitlity functions and package initialization.

```python
from functools import lru_cache
import pkg_resources


from .settings import Settings
from .tid_auth import TidUserAuth

@lru_cache()
def get_settings() -> Settings:
    """This utilized lru_cache so that as long as Settings doesn't change it will always return the same settings object

    Returns
    -------
    Settings
        settings
    """
    retval = Settings()
    return retval

@lru_cache()
def get_tid_auth() -> TidUserAuth:
    """This utilized lru_cache so that as long as TidAuth doesn't change it will always return the same TidAuth object

    Returns
    -------
    TidUserAuth
        TidUserAuth
    """
    settings = get_settings()
    retval = TidUserAuth(
        client_id=settings.tid_client_id,
        app_name=settings.tid_client_name,
        base_url=settings.tid_base_url,
        scopes=settings.tid_scopes
        )
    return retval

def get_my_package_version() -> str:
    """
    Returns only the version of the package.

    This is a convience function that I use so that I can copy and paste this file to many projects without changing the name

    Returns:
        str: The version string of the current package.
    """
    pkg_version = pkg_resources.get_distribution(__name__).version
    return f"{pkg_version}"

def get_my_package_name() -> str:
    """
    Returns only the name of the package.

    This is a convience function that I use so that I can copy and paste this file to many projects without changing the name

    Returns:
        str: The name of the current package with dashes instead of underscores.
    """
    pkg_name = pkg_resources.get_distribution(__name__).project_name
    return f"{pkg_name}".replace('_','-')

```

### src/fastapi_template/tid_auth.py

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


### src/fastapi_template/gen_env_template.py

generates a template .env file for the project.

```python
import argparse
from .settings import Settings

def generate_env_template(output_path: str = ".env.template") -> None:
    """
    Generate a template .env file based on the Settings class.

    Parameters
    ----------
    output_path : str
        Path where the .env.template file will be saved. Default is ".env.template".

    Returns
    -------
    None
        Writes the template to the specified file.
    """


    # Create a settings instance with default values
    settings = Settings()

    # Get the environment prefix from model_config
    env_prefix = settings.model_config.get('env_prefix', '').upper()

    # Generate the template content
    template_lines = []
    template_lines.append("# Template environment configuration for tid-sample-api")
    template_lines.append("# Copy this file to .env and modify as needed")
    template_lines.append("")

    # Get fields from Settings class annotations
    for field_name, field_type in Settings.__annotations__.items():
        if field_name != 'model_config' and not field_name.startswith('_'):
            # Get the default value from the settings instance
            field_value = getattr(settings, field_name, '')

            # Add the field to the template
            template_lines.append(f"# {field_name} ({field_type.__name__})")
            template_lines.append(f"{env_prefix}{field_name.upper()}={field_value}")
            template_lines.append("")

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(template_lines))

    print(f"ENV template file generated at: {output_path}")

def main():
    """Command line interface to generate .env.template file."""

    parser = argparse.ArgumentParser(description="Generate a .env.template file from Settings")
    parser.add_argument("--output", "-o", default=".env.template",
                        help="Output file path (default: .env.template)")

    args = parser.parse_args()
    generate_env_template(args.output)

if __name__ == "__main__":
    main()
```

### src/fastapi_template/dev.py
Development server for the FastAPI application.

```python
from .create_app import create_app

dev_app = create_app()

```
