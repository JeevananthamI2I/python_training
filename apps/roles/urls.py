from django.urls import path
from .views import (
    RoleListView, RoleCreateView, RoleDetailView,
    RoleRestoreView, RoleToggleStatusView, RoleDeletedListView
)

urlpatterns = [
    # List and create roles
    path('', RoleListView.as_view(), name='role-list'),
    path('create/', RoleCreateView.as_view(), name='role-create'),
    
    # Detail operations
    path('<uuid:pk>/', RoleDetailView.as_view(), name='role-detail'),
    
    # Custom actions
    path('<uuid:pk>/restore/', RoleRestoreView.as_view(), name='role-restore'),
    path('<uuid:pk>/toggle-status/', RoleToggleStatusView.as_view(), name='role-toggle-status'),
    
    # List deleted roles
    path('deleted/', RoleDeletedListView.as_view(), name='role-deleted-list'),
]
