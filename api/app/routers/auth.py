from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.dependencies import get_db, get_current_active_admin, get_current_active_user, get_api_key
from app.schemas.user import AuthRequest, UserCreate, PasswordResetRequest, UserUpdateRequest, Token
from app.services.auth_service import (
    register_new_user, login_user, refresh_access_token,
    reset_user_password, delete_user, disable_user, modify_user
)
from app.utils.jwt_util import jwt_service

router = APIRouter()


@router.post("/register",
             response_model=Token,
             status_code=status.HTTP_201_CREATED,
             summary="Register a new user",
             responses={
                 201: {
                     "description": "User successfully registered and JWT tokens provided.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "username": "newuser",
                                 "email": "newuser@example.com",
                                 "password": "strongpassword123",
                                 "role": "User"
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Email already registered.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Email already registered."
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             })
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with a username, email, and password.
    This endpoint will also send an email verification message.
    """
    return register_new_user(request, user, db)


@router.post("/login",
             include_in_schema=True,
             response_model=Token,
             summary="Login a user",
             responses={
                 200: {
                     "description": "User logged in successfully with access and refresh tokens returned.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                 "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                 "token_type": "bearer"
                             }
                         }
                     }
                 },
                 401: {
                     "description": "Incorrect email or password.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid email or password."
                             }
                         }
                     }
                 },
                 403: {
                     "description": "Account is suspended.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Account is suspended."
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             })
def login(auth_request: AuthRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and provide JWT tokens if successful.
    """
    return login_user(auth_request, db)


@router.post("/refresh",
             response_model=Token,
             summary="Refresh the JWT token",
             responses={
                 200: {
                     "description": "Access token successfully refreshed.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                 "token_type": "bearer"
                             }
                         }
                     }
                 },
                 403: {
                     "description": "Invalid or no refresh token provided.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Authorization header missing"
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             },
             dependencies=[Depends(get_current_active_user)])
def refresh_token(refresh_token: str = Depends(jwt_service.verify_refresh_token),
                  db: Session = Depends(get_db)):
    """
    Refresh an expired access token using a valid refresh token.
    """
    return refresh_access_token(refresh_token, db)


@router.post("/reset_password",
             summary="Reset user password",
             responses={
                 200: {
                     "description": "Password reset successfully. A confirmation email has been sent.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Password reset successfully"
                             }
                         }
                     }
                 },
                 404: {
                     "description": "User not found with provided email.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "User not found"
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             })
def reset_password(password_reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Allow a user to reset their password, requiring their email and new password.
    Sends a confirmation email upon successful reset.
    """
    return reset_user_password(password_reset_request.email, password_reset_request.new_password, db)


@router.delete("/delete/{user_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a user",
               responses={
                   204: {
                       "description": "User deleted successfully.",
                       "content": {}
                   },
                   404: {
                       "description": "User not found.",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "User not found"
                               }
                           }
                       }
                   },
                   422: {
                       "description": "Invalid data.",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Invalid body format"
                               }
                           }
                       }
                   }
               },
               dependencies=[Depends(get_current_active_admin)])
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a user from the database.
    """
    delete_user(user_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/disable/{user_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Enable or disable a user",
            responses={
                204: {
                    "description": "User status updated successfully.",
                    "content": {}
                },
                404: {
                    "description": "User not found.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "User not found"
                            }
                        }
                    }
                },
                422: {
                    "description": "Invalid data.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Invalid body format"
                            }
                        }
                    }
                }
            },
            dependencies=[Depends(get_current_active_admin), Depends(get_api_key)])
def disable_user_endpoint(user_id: int, enabled: bool, db: Session = Depends(get_db)):
    """
    Enable or disable a user account based on the boolean 'enabled' parameter.
    """
    disable_user(user_id, enabled, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/modify/{user_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Modify user details",
            responses={
                204: {"description": "User details updated successfully.",
                      "content": {}
                      },
                404: {
                    "description": "User not found.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "User not found"
                            }
                        }
                    }
                },
                422: {
                    "description": "Invalid data.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Invalid body format"
                            }
                        }
                    }
                }
            },
            dependencies=[Depends(get_current_active_admin), Depends(get_api_key)])
def modify_user_endpoint(user_id: int, update_request: UserUpdateRequest, db: Session = Depends(get_db)):
    """
    Update user details such as username, email, and potentially other profile information.
    """
    modify_user(user_id, update_request.dict(exclude_unset=True), db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
