# API Routes


## src/fastapi_template/routers/__init__.py

Router package initialization.

```python
from .api import api_router

# convienence method to get all routers
ROUTER_LIST = [api_router]

```

## src/fastapi_template/routers/api.py

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

