from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include

from books.views import *
from schedule.views import *
from schedule.urls import *


router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'books', BookViewSet)
router.register(r'blocks', StudyBlockViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/', include('users.auth_urls')),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('schedule/', include('schedule.urls')),
    path('api/', include(router.urls)),
]
