from django.urls import path
from .views import CustomTokenView, UserListCreateView, UserDeleteView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<str:tr_number>/', UserDeleteView.as_view(), name='user-delete'),
]
