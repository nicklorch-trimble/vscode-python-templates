# VS Code Configuration

Documentation for editor and debug settings.

## .vscode/launch.json

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

## .vscode/settings.json

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
