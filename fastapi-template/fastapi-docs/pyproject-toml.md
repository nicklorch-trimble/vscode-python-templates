# Project Configuration (pyproject.toml)

This file defines the project metadata, dependencies, development tools, and build system. It's the central configuration file for Python projects using modern packaging tools.

## File Content

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

## Key Components

- **Build System**: Uses setuptools for building packages
- **Project Metadata**: Defines name, version, description and author information
- **Dependencies**: Lists required packages like fastapi, pydantic_settings, etc.
- **Optional Dependencies**: Development tools like bump-my-version
- **Entry Points**: Defines console scripts for running the application and generating environment templates
