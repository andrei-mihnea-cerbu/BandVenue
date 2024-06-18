from .auth_service import AuthService
from .artist_service import ArtistService
from .event_service import EventService
from .user_service import UserService

from app.dependencies import get_db

user_service_class = UserService(get_db())
auth_service_class = AuthService(get_db())
artist_service_class = ArtistService(get_db())
event_service_class = EventService(get_db())