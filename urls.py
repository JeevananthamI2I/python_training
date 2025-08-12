"""
URL configuration for meditrack360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.defaults import page_not_found
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_not_found(request, exception=None):
    """Custom 404 handler for API endpoints."""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'success': False,
            'error': 'API endpoint not found',
            'code': 'endpoint_not_found',
            'message': 'The requested API endpoint does not exist',
            'details': {
                'path': request.path,
                'method': request.method,
                'correct_format': '/api/v1/{resource}/',
                'available_endpoints': [
                    '/api/v1/auth/',
                    '/api/v1/organizations/',
                    '/api/v1/users/',
                    '/api/v1/roles/',
                    '/api/v1/addresses/',
                    '/api/v1/patients/',
                    '/api/v1/visits/'
                ]
            }
        }, status=404)
    return page_not_found(request, exception)

def redirect_to_api(request, resource):
    """Redirect common mistakes to the correct API endpoint."""
    return JsonResponse({
        'success': False,
        'error': 'Incorrect API endpoint',
        'code': 'incorrect_endpoint',
        'message': f'Use /api/v1/{resource}/ instead of /{resource}',
        'details': {
            'current_path': f'/{resource}',
            'correct_path': f'/api/v1/{resource}/',
            'documentation': '/api/docs/'
        }
    }, status=400)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Redirect common mistakes
    path('organizations', lambda request: redirect_to_api(request, 'organizations')),
    path('users', lambda request: redirect_to_api(request, 'users')),
    path('patients', lambda request: redirect_to_api(request, 'patients')),
    path('visits', lambda request: redirect_to_api(request, 'visits')),
    path('roles', lambda request: redirect_to_api(request, 'roles')),
    path('addresses', lambda request: redirect_to_api(request, 'addresses')),
    path('auth', lambda request: redirect_to_api(request, 'auth')),
    
    # API v1 endpoints
    path('api/v1/', include([
        path('auth/', include('apps.authentication.urls')),
        path('organizations/', include('apps.organizations.urls')),
        path('users/', include('apps.users.urls')),
        path('roles/', include('apps.roles.urls')),
        path('addresses/', include('apps.addresses.urls')),
        path('patients/', include('apps.patients.urls')),
        path('visits/', include('apps.visits.urls')),
    ])),
]

# Set custom 404 handler
handler404 = 'meditrack360.urls.api_not_found'
