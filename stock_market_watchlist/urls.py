from django.contrib import admin
from django.urls import include, path
from api.views import UserRegistrationView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='api_token_auth'),
    
    # Login as the default page
    path('', LoginView.as_view(), name='default_login'),
]
