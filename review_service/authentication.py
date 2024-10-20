from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Override to get the user from custom fields (e.g., email).
        """
        user_id = validated_token['user_id']
        user = User.objects.filter(id=user_id).first()  # Fetch the user
        return user