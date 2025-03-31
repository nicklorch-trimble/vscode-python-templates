# FastAPI Template

This sample repo contains the recommended structure for a Python FastAPI project. In this sample, we use `fastapi` to build a web application and the `pytest` to run tests.

The code in this repo aims to follow Python style guidelines as outlined in [PEP 8](https://peps.python.org/pep-0008/).

## Set up instructions

This sample makes use of Dev Containers, in order to leverage this setup, make sure you have [Docker installed](https://www.docker.com/products/docker-desktop).

To successfully run this example, we recommend the following VS Code extensions:

- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

In addition to these extension there a few settings that are also useful to enable. You can enable to following settings by opening the Settings editor (`Ctrl+,`) and searching for the following settings:

- Python > Analysis > **Type Checking Mode** : `basic`
- Python > Analysis > Inlay Hints: **Function Return Types** : `enable`
- Python > Analysis > Inlay Hints: **Variable Types** : `enable`

## Running the sample
- Open the template folder in VS Code (**File** > **Open Folder...**)
- Create a virtual environment using the command `python -m venv venv`
- Activate the virtual environment using the command `source venv/bin/activate` on MacOS/Linux or `venv\Scripts\activate` on Windows
- Install the dependencies using the command `pip install -e .[dev]`
- Run the app using the Run and Debug view or by pressing `F5`
- You can also run the app by typing `fastapi-template -r` in the terminal. `-r` is the alias for `--reload` and it will automatically reload the server when you make changes to the code.
- `Ctrl + click` on the URL that shows up on the terminal to open the running application
- Test the API functionality by navigating to `/docs` URL to view the Swagger UI
- Configure your Python test in the Test Panel or by triggering the **Python: Configure Tests** command from the Command Palette
- Run tests in the Test Panel or by clicking the Play Button next to the individual tests in the `test_main.py` file