from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['tr_number'] = user.tr_number
        token['role'] = user.role  # Used by frontend for redirection
        return token

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
