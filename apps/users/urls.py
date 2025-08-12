from django.urls import path
from .views import (
    UserRegistrationView, UserListView, UserCreateView, UserDetailView, 
    UserRestoreView, UserChangePasswordView, UserDeletedListView
)

urlpatterns = [
    # Registration endpoint (POST /users) - HMS Flow Step 1 & 3
    path('', UserRegistrationView.as_view(), name='user-register'),
    
    # List users (GET /users/list)
    path('list/', UserListView.as_view(), name='user-list'),
    
    # Create user with authentication
    path('create/', UserCreateView.as_view(), name='user-create'),
    
    # Detail operations
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Custom actions
    path('<int:pk>/restore/', UserRestoreView.as_view(), name='user-restore'),
    path('<int:pk>/change-password/', UserChangePasswordView.as_view(), name='user-change-password'),
    
    # List deleted users
    path('deleted/', UserDeletedListView.as_view(), name='user-deleted-list'),
] 