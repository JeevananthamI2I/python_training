from django.urls import path
from .views import (
    AddressListView, AddressCreateView, AddressDetailView,
    AddressRestoreView, AddressDeletedListView, AddressCitiesView, AddressStatesView
)

urlpatterns = [
    # List and create addresses
    path('', AddressListView.as_view(), name='address-list'),
    path('create/', AddressCreateView.as_view(), name='address-create'),
    
    # Detail operations
    path('<uuid:pk>/', AddressDetailView.as_view(), name='address-detail'),
    
    # Custom actions
    path('<uuid:pk>/restore/', AddressRestoreView.as_view(), name='address-restore'),
    
    # List deleted addresses
    path('deleted/', AddressDeletedListView.as_view(), name='address-deleted-list'),
    
    # Utility endpoints
    path('cities/', AddressCitiesView.as_view(), name='address-cities'),
    path('states/', AddressStatesView.as_view(), name='address-states'),
] 