import jwt
from jwt.exceptions import InvalidSignatureError
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import Token
from user.models import User


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"
    model = Token

    def authenticate(self, request):
        auth = request.headers.get("Authorization", "").split()
        if not auth or auth[0].lower() != self.keyword.lower():
            return None

        if len(auth) == 1:
            raise AuthenticationFailed("Invalid token header. No credentials provided.")
        elif len(auth) > 2:
            raise AuthenticationFailed("Invalid token header. Token string should not contain spaces.")

        try:
            token = auth[1]
            decoded_token = jwt.decode(token, "secret", algorithms=["HS256"], verify=False)
        except UnicodeError:
            raise AuthenticationFailed("Invalid token header. Token string should not contain invalid characters.")

        except InvalidSignatureError:
            raise AuthenticationFailed("Invalid token header. Token signature is invalid.")

        _token = self.model.objects.filter(token=token).first()
        user = User.objects.get(id=decoded_token["user"])
        return (user, _token)
