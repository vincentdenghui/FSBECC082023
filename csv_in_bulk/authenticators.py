from django.contrib.auth import authenticate, login
import base64


def basic_auth_logged_in(request):
    """"
    Authenticate a user using the basic authentication.
    The user will be logged-in in the request object upon successful authentication.

    """
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == "basic":
            uname, passwd = base64.b64decode(auth[1].encode()).decode('utf-8').split(':')
            user = authenticate(username=uname, password=passwd)
            if user and user.is_active:
                login(request, user)
                request.user = user
                return True
    return False