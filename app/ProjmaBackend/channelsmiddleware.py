from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
# from rest_framework_simplejwt.state import User
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from board.models import Board
from asgiref.sync import sync_to_async


@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
    except:
        user = AnonymousUser()
    return user


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
            # boardid = parse_qs(scope["query_string"].decode("utf8"))["board"][0]
            # boardid = int(boardid)
        except:
            return None

        try:
            UntypedToken(token)
            # board = await sync_to_async(Board.objects.get)(id=boardid)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            # print(e)
            return None

        #  Then token is valid, decode it
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        scope["user"] = await get_user(validated_token=decoded_data)
        # scope["board"] = board
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
