from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import settings
from app.database import engine, SessionLocal, Base
from app.dependencies import get_api_key
from app.routers import artists, events, auth
from app.utils.email_util import email_service
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
    - `DELETE /auth/delete/{user_id}`: Permanently deletes a user from the database.
    - `PUT /auth/disable/{user_id}`: Enables or disables a user account based on the provided boolean parameter.
    - `PUT /auth/modify/{user_id}`: Updates user details such as username and email.

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


@app.on_event("startup")
def startup_event():
    # Database connection check on startup
    check_database_connection()
    if settings.MODE == "Development":
        app.openapi = custom_openapi
    # Send startup email notification
    try:
        email_service.send_startup_email()
        logger.info("Startup email sent successfully.")
    except Exception as e:
        logger.error("Failed to send startup email: %s", str(e))
        raise HTTPException(status_code=500, detail="SMTP connection failed: " + str(e))


def check_database_connection():
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        logger.info("Database connection verified successfully.")
    except SQLAlchemyError as e:
        logger.error("Database connection failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Database connection failed: " + str(e))


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Band Venue API",
        version="1.0.0",
        description=app.description,
        routes=app.routes
    )
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        },
        "APIKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY"
        }
    }
    openapi_schema["security"] = [
        {"BearerAuth": []},
        {"APIKeyAuth": []}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Custom 422 error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid body format"}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth.router,
                   prefix="/auth",
                   tags=["auth"],
                   dependencies=[Depends(get_api_key)])

app.include_router(artists.router,
                   prefix="/artists",
                   tags=["artists"],
                   dependencies=[Depends(get_api_key)])

app.include_router(events.router,
                   prefix="/events",
                   tags=["events"],
                   dependencies=[Depends(get_api_key)])


Base.metadata.create_all(bind=engine)
