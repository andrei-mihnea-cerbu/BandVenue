from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
from app.database import engine, SessionLocal
from app.database import Base
from app.routers import artists, events, auth
from app.utils.email_service import email_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Band Venue API",
    description="""
    This API allows you to manage band venues and events. 

    To enable the HTTPS version of the API, please request the server.ca-bundle from the admin to use in production.
    In the case of development, please use the HTTP version only in the UI development.

    ## Authentication

    - `POST /auth/authenticate`: Authenticates using the password from the config.
    - `POST /auth/register`: Register a new user with username, password, and email.
    - `POST /auth/login`: Login using email and password to receive an access token and a refresh token.
    - `POST /auth/refresh`: Refresh the JWT token using the refresh token.
    - `POST /auth/reset_password`: Reset the user's password by providing the email and new password.

    ### Authentication Workflow

    1. **Register**: Create a new user by providing a username, password, and email.
    2. **Login**: Obtain an access token and refresh token by providing the email and password.
    3. **Authenticated Requests**: Use the access token in the `Authorization` header for authenticated requests.
    4. **Token Refresh**: Use the refresh token to obtain a new access token when the current one expires.

    ### Token Information

    - **API Key**: Include the API key `9542752b-4897-407b-acdd-4e8fcd68d7e8` in the `X-API-KEY` header for authenticated requests.
    - **JWT**: The access token is a JWT that contains the following claims:
        - `sub`: The username.
        - `id`: The user ID.
        - `email`: The user's email.
        - `role`: The user's role (e.g., User, Admin).
    - **JWT Decoding**: Use the following details to decode the JWT:
        - **Secret Key**: `c7b6a5e06fad2dd3363fccf2fa18f93706c3cd2a6d9cebbf41ec545c525f59e4`
        - **Algorithm**: `HS256`

    ### Admin Credentials

    - **Username**: `admin`
    - **Email**: `admin@thevoodoochildband.com`
    - **Password**: `VoodooRules123!`

    ## Artist Endpoints

    - `GET /artists`: Get all artists.
    - `POST /artists`: Create a new artist.
    - `GET /artists/{artist_id}`: Get a specific artist by ID.
    - `PUT /artists/{artist_id}`: Update a specific artist by ID.
    - `DELETE /artists/{artist_id}`: Delete a specific artist by ID.

    ## Event Endpoints

    You can add the following types of events: - **Festival**: Includes details such as accommodation, transport, 
    merchandise, and artist payment. - **Personal Concert**: Includes details such as accommodation, transport, 
    ticket price, number of physical tickets, number of electronic tickets, electronic ticket fee, and culture tax.

    - `POST /events`: Create a new event with details.
    - `GET /events`: Get all events.
    - `GET /events/{event_id}`: Get a specific event by ID.
    - `PUT /events/{event_id}`: Update a specific event by ID.
    - `DELETE /events/{event_id}`: Delete a specific event by ID.
    """,
    version="1.0.0"
)


def check_database_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        logger.info("Database connection verified successfully.")
    except SQLAlchemyError as e:
        logger.error("Database connection failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Database connection failed: " + str(e))
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    check_database_connection()
    try:
        email_service.send_startup_email()
        logger.info("Startup email sent successfully.")
    except Exception as e:
        logger.error("Failed to send startup email: %s", str(e))
        raise HTTPException(status_code=500, detail="SMTP connection failed: " + str(e))


if settings.MODE == "Development":
    from fastapi.openapi.utils import get_openapi


    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Band Venue API",
            version="1.0.0",
            description=app.description,
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema


    app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == settings.API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    artists.router,
    prefix="/artists",
    tags=["artists"],
    dependencies=[Depends(get_api_key)],
)

app.include_router(
    events.router,
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(get_api_key)],
)

Base.metadata.create_all(bind=engine)
