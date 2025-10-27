from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.auth_urls')),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('schedule/', include('schedule.urls')),
]
