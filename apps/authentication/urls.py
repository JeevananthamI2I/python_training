from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 