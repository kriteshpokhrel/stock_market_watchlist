from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from api.views import UserRegistrationView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='api_token_auth'),
]
