from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    MODE: str = "dev"
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    # ALLOWED_ORIGIN: str
    # OIDC_ISSUER: HttpUrl
    # OIDC_CLIENT_ID: str
    # OIDC_JWKS_URI: HttpUrl
    # ADMIN_LIST: str = "0000000000000000000,"

    class Config:
        env_file = "../.env"


SETTINGS = Settings()
