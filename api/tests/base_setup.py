from rest_framework.test import APITestCase
from ..serializers import UserRegistrationSerializer

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.admin_data = {
            'username': 'admin', 'password': 'AdminPass123', 'email': 'admin@example.com', 'name': 'Admin'
        }
        self.user_data = {
            'username': 'user', 'password': 'UserPass123', 'email': 'user@example.com', 'name': 'Regular User'
        }

        self.admin_user = self._create_user(self.admin_data, is_superuser=True, is_staff=True)
        self.regular_user = self._create_user(self.user_data)

    def _create_user(self, data, **extra_fields):
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        for attr, val in extra_fields.items():
            setattr(user, attr, val)
        user.save()
        return user
    
    def _create_user(self, data, **extra_fields):
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        for attr, val in extra_fields.items():
            setattr(user, attr, val)
        user.save()
        return user

    def authenticate(self, user):
        self.client.force_authenticate(user=user)