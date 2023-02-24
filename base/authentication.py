# Reference: https://stackoverflow.com/questions/47274670/django-rest-auth-use-cookie-instead-of-authorization-header
from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
import urllib.parse

class TokenAuthSupportCookie(BaseTokenAuth):
    """
    Extend the TokenAuthentication class to support cookie based authentication
    """
    def authenticate(self, request):
        # Check if 'auth_token' is in the request cookies.
        # Give precedence to 'Authorization' header.

        try: # Will authenticate a valid token stored in cookie
            if 'auth_token' in request.COOKIES:
                return self.authenticate_credentials(
                urllib.parse.unquote_plus(request.COOKIES.get('auth_token')))
        except:
            pass

        return super().authenticate(request)# Will authenticate via Authorization header (or return None when no authentication is provided)