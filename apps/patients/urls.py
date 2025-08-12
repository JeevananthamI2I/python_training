from django.urls import path
from .views import (
    PatientListView, PatientCreateView, PatientDetailView,
    PatientRestoreView, PatientMedicalHistoryView, PatientDeletedListView, PatientBloodGroupsView
)

urlpatterns = [
    # List and create patients
    path('', PatientListView.as_view(), name='patient-list'),
    path('create/', PatientCreateView.as_view(), name='patient-create'),
    
    # Detail operations
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    
    # Custom actions
    path('<int:pk>/restore/', PatientRestoreView.as_view(), name='patient-restore'),
    path('<int:pk>/medical-history/', PatientMedicalHistoryView.as_view(), name='patient-medical-history'),
    
    # List deleted patients
    path('deleted/', PatientDeletedListView.as_view(), name='patient-deleted-list'),
    
    # Utility endpoints
    path('blood-groups/', PatientBloodGroupsView.as_view(), name='patient-blood-groups'),
] 