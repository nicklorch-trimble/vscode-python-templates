# Project Structure

The fastapi template project follows a well-organized structure to separate concerns and improve maintainability.

```
fastapi-template
├── .vscode                    # VS Code configuration
│   ├── launch.json             # Debug configurations
│   └── settings.json           # Editor settings
├── src                        # Source code
│   └── fastapi_template       # Main package
│       ├── data_models        # Pydantic models
│       │   ├── __init__.py
│       │   └── auth_models.py  # Authentication models
│       ├── routers            # API route definitions
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

This structure follows modern Python project organization principles:

- Source code is contained within a `src` directory
- Main application code is in a package named after the project
- Configuration files are at the project root
- Components are organized by function (routers, data models)
