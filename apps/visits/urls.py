from django.urls import path
from .views import (
    VisitListView, VisitCreateView, VisitDetailView,
    VisitRestoreView, VisitCompleteView, VisitCancelView,
    VisitDeletedListView, VisitUpcomingListView, VisitTodayListView
)

urlpatterns = [
    # List and create visits
    path('', VisitListView.as_view(), name='visit-list'),
    path('create/', VisitCreateView.as_view(), name='visit-create'),
    
    # Detail operations
    path('<uuid:pk>/', VisitDetailView.as_view(), name='visit-detail'),
    
    # Custom actions
    path('<uuid:pk>/restore/', VisitRestoreView.as_view(), name='visit-restore'),
    path('<uuid:pk>/complete/', VisitCompleteView.as_view(), name='visit-complete'),
    path('<uuid:pk>/cancel/', VisitCancelView.as_view(), name='visit-cancel'),
    
    # List deleted visits
    path('deleted/', VisitDeletedListView.as_view(), name='visit-deleted-list'),
    
    # Special lists
    path('upcoming/', VisitUpcomingListView.as_view(), name='visit-upcoming-list'),
    path('today/', VisitTodayListView.as_view(), name='visit-today-list'),
] 