# Application Factory (create_app.py)

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
