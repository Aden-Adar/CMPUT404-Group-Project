# # Reference: https://stackoverflow.com/questions/47274670/django-rest-auth-use-cookie-instead-of-authorization-header
# from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.authentication import BasicAuthentication
import urllib.parse
import base64

class BasicAuthSupportCookie(BasicAuthentication):
    """
    Extend the BasicAuthentication class to support cookie based authentication
    """

    def authenticate(self, request):
        # Check if 'auth_token' is in the request cookies.
        # Give precedence to 'Authorization' header.

        try:
            auth_encoded = urllib.parse.unquote_plus(request.COOKIES.get('auth_token'))
            auth_decoded = base64.b64decode(auth_encoded.encode("ascii"))

            username, password = auth_decoded.decode("ascii").split(":")
            if 'auth_token' in request.COOKIES:
                return self.authenticate_credentials(username, password)
        except:
            pass

        return super().authenticate(request)# Will authenticate via Authorization header (or return None when no authentication is

