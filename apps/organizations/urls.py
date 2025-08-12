from django.urls import path
from .views import (
    OrganizationCreateView, OrganizationListView, OrganizationDetailView,
    OrganizationRestoreView, OrganizationStatusView, OrganizationDeletedListView
)

urlpatterns = [
    # Create organization endpoint (POST /organizations) - HMS Flow Step 2
    path('', OrganizationCreateView.as_view(), name='organization-create'),
    
    # List organizations (GET /organizations/list)
    path('list/', OrganizationListView.as_view(), name='organization-list'),
    
    # Detail operations
    path('<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    
    # Custom actions
    path('<int:pk>/restore/', OrganizationRestoreView.as_view(), name='organization-restore'),
    path('<int:pk>/status/', OrganizationStatusView.as_view(), name='organization-status'),
    
    # List deleted organizations
    path('deleted/', OrganizationDeletedListView.as_view(), name='organization-deleted-list'),
] 