# Package Initialization

Documentation for common utility functions in the package __init__.py file.

## src/fastapi_template/__init__.py

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