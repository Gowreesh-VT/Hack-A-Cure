import secrets
from typing import Annotated, Any, Literal, Union, List
from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> Union[List[str], str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use .env file - will check current dir and parent dirs
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        case_sensitive=True,
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        Union[List[AnyUrl], str], BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> List[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str
    SENTRY_DSN: Union[HttpUrl, None] = None

    SQLALCHEMY_DATABASE_URI: str

    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_FIRST_NAME: str
    FIRST_SUPERUSER_LAST_NAME: str
    
    JWT_USER: EmailStr
    JWT_USER_PASSWORD: str
    JWT_USER_FIRST_NAME: str
    JWT_USER_LAST_NAME: str
    
    TIME_ZONE : str
    
    # LLM RAG - supports OpenAI, Azure OpenAI, and Google Vertex AI
    ## OpenAI (standard) - optional if using Google Vertex AI
    OPENAI_API_KEY: Union[str, None] = None
    OPENAI_MODEL_NAME: Union[str, None] = None
    OPENAI_EMBEDDINGS_NAME: Union[str, None] = None
    
    ## Azure OpenAI (optional - set USE_AZURE=true to enable)
    USE_AZURE: bool = False
    AZURE_OPENAI_API_KEY: Union[str, None] = None
    AZURE_OPENAI_ENDPOINT: Union[str, None] = None
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_OPENAI_DEPLOYMENT_NAME: Union[str, None] = None
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: Union[str, None] = None
    
    ## Google Cloud Vertex AI (optional - set USE_GOOGLE_VERTEX=true to enable)
    USE_GOOGLE_VERTEX: bool = False
    GOOGLE_CLOUD_PROJECT: Union[str, None] = None
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    GOOGLE_VERTEX_MODEL: str = "gemini-1.0-pro"
    GOOGLE_VERTEX_EMBEDDING_MODEL: str = "text-embedding-004"
    
    ## Google Gemini API (direct API - simpler than Vertex AI)
    USE_GEMINI_API: bool = False
    GOOGLE_API_KEY: Union[str, None] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    ## Qdrant
    QDRANT_COLLECTION_NAME: str
    QDRANT_API_KEY: str
    QDRANT_URL: str


settings = Settings()  # type: ignore
