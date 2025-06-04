from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.db import close_old_connections

@database_sync_to_async
def get_user(validated_token):
    try:
        jwt_auth = JWTAuthentication()
        user = jwt_auth.get_user(validated_token)
        return user
    except Exception:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])

        # Check if "authorization" header is present
        auth_header = headers.get(b"authorization", b"").decode()
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                validated_token = JWTAuthentication().get_validated_token(token)
                scope["user"] = await get_user(validated_token)
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        close_old_connections()
        return await super().__call__(scope, receive, send)
