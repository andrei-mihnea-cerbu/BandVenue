from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.dependencies import get_db
from app.schemas.user import UserUpdateRequest
from app.services import user_service_class

router = APIRouter()


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
               })
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a user from the database.
    """
    user_service_class.delete_user(user_id, db)
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
            })
def disable_user_endpoint(user_id: int, enabled: bool, db: Session = Depends(get_db)):
    """
    Enable or disable a user account based on the boolean 'enabled' parameter.
    """
    user_service_class.disable_user(user_id, enabled, db)
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
            })
def modify_user_endpoint(user_id: int, update_request: UserUpdateRequest, db: Session = Depends(get_db)):
    """
    Update user details such as username, email, and potentially other profile information.
    """
    user_service_class.modify_user(user_id, update_request.dict(exclude_unset=True), db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
