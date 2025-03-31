"""
This module creates a FastAPI application instance specifically for development environments.

It uses the `create_app` function imported from the `.create_app` module to instantiate the application.
The `dev_app` variable is exposed at module level, which allows Uvicorn to import and use it for hot reloading.

When using Uvicorn's hot reloading feature (--reload flag), Uvicorn looks for a global application instance
that it can reload whenever code changes are detected. By exposing `dev_app` at the module level,
developers can reference it using the format `module:app_instance` (e.g., `tid_sample_api.dev:dev_app`)
when starting Uvicorn.

Example usage with Uvicorn:
    uvicorn tid_sample_api.dev:dev_app --reload
"""
from .create_app import create_app

dev_app = create_app()
