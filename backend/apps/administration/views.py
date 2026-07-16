import logging

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from core.responses import error_response, success_response
from core.throttles import AdminLoginRateThrottle

from .docs import admin_login_doc
from .serializers import AdminLoginSerializer, AdminUserSerializer
from .services import admin_login

logger = logging.getLogger("authentication")


class AdminLoginAPIView(APIView):
    """Handle a request to authenticate an administrator.

    Validates credentials and ensures the user has staff or superuser privileges
    before issuing JWT tokens.
    """

    permission_classes = []
    throttle_classes = [AdminLoginRateThrottle]

    @admin_login_doc
    def post(self, request):
        """Authenticate an admin and return JWT tokens.

        Args:
            request: The incoming HTTP request. Expected body:
                - email (str): Admin's email address.
                - password (str): Admin's password.

        Returns:
            A success response containing the access and refresh tokens,
            or a 401 error response if authentication fails.
        """
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = admin_login(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
        except AuthenticationFailed as e:
            logger.warning(
                f"Failed admin login attempt for email: {serializer.validated_data['email']}"
            )
            return error_response(
                message=str(e.detail) if hasattr(e, "detail") else str(e),
                status_code=401,
            )

        user = result["user"]
        logger.info(f"Successful admin login for user: {user.id}")

        return success_response(
            message="Admin login successfully",
            data={
                "access": result["access"],
                "refresh": result["refresh"],
                "user": AdminUserSerializer(user).data,
            },
        )
