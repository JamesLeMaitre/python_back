import secrets
from typing import Union, List, Optional, Dict, Any

from databases import DatabaseURL
from pydantic import AnyHttpUrl, BaseSettings, validator, EmailStr


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000"]
    PROJECT_NAME: str = "prod"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(self, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = None
    MYSQL_SERVER: str = "localhost"
    MYSQL_DB: str = "data_db"
    SQLALCHEMY_DATABASE_URI:  None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(self, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return DatabaseURL(
            f"mysql://{values['MYSQL_USER']}:{values['MYSQL_PASSWORD']}@{values['MYSQL_SERVER']}/{values['MYSQL_DB']}"
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
