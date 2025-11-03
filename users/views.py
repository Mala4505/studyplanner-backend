from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import User
from .serializers import UserSerializer, UserSignupSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # ✅ disables JWT
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['tr_number'] = user.tr_number
        token['role'] = user.role  # ✅ This line ensures role is included
        return token


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = serializer.validated_data
        print("Generated token for user:", user.tr_number, "with role:", user.role)
            
        return Response({
            'access': token['access'],
            'refresh': token['refresh'],
            'role': user.role  # ✅ Include role here
        })

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, tr_number):
        try:
            user = User.objects.get(tr_number=tr_number)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, tr_number):
        try:
            user = User.objects.get(tr_number=tr_number)
            data = request.data
            if 'password' in data:
                user.set_password(data['password'])
            if 'role' in data:
                user.role = data['role']
            user.save()
            return Response({'message': 'User updated successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

