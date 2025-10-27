from django.urls import path
from .views import UserListCreateView, UserDeleteView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<str:tr_number>/', UserDeleteView.as_view(), name='user-delete'),
]
