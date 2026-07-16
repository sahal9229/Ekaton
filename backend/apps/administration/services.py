from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def admin_login(email, password):
    """Authenticate an admin user and return JWT tokens.

    Validates credentials and ensures the user has staff or superuser
    privileges.

    Args:
        email: The admin's email address.
        password: The admin's raw password.

    Returns:
        dict: Containing 'user' instance, 'refresh' token, and 'access' token.

    Raises:
        AuthenticationFailed: If credentials are invalid or user lacks admin privileges.
    """

    user = authenticate(email=email, password=password)

    if user is None:
        raise AuthenticationFailed("Invalid email or password.")

    if not (user.is_superuser or user.is_staff):
        raise AuthenticationFailed("Only administrators can log in.")

    refresh = RefreshToken.for_user(user)

    return {"user": user, "refresh": str(refresh), "access": str(refresh.access_token)}
