from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import AccessToken
# from datetime import datetime
# import pytz

User = get_user_model()


def create_jwt_pair_for_user(user: User):  # type: ignore
    refresh = RefreshToken.for_user(user)
    # decoded_token = AccessToken(token=str(refresh.access_token))
    # expiration_timestamp = decoded_token['exp']
    # lagos_timezone = pytz.timezone("Africa/Lagos")
    # expires_at_datetime = datetime.fromtimestamp(expiration_timestamp, tz=lagos_timezone)
    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
    return tokens
