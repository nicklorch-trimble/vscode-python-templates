# src/fastapi_template/main.py

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
