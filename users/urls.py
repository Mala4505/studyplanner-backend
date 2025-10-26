from django.urls import path
from .views import CustomTokenView

urlpatterns = [
    path('login/', CustomTokenView.as_view(), name='token_obtain_pair'),
]
