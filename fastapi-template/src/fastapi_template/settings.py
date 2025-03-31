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

