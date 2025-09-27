"""
URL configuration for hortechia_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from gardens.views import GardenViewSet, PlantViewSet, CultivationPlanViewSet
from ai_recommendations.views import AIRecommendationViewSet
from core.views import home, api_status

# Router para API
router = DefaultRouter()
router.register(r'gardens', GardenViewSet, basename='garden')
router.register(r'plants', PlantViewSet, basename='plant')
router.register(r'cultivation-plans', CultivationPlanViewSet, basename='cultivation-plan')
router.register(r'ai-recommendations', AIRecommendationViewSet, basename='ai-recommendation')

urlpatterns = [
    # Frontend
    path('', home, name='home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/v1/', include(router.urls)),
    path('api/v1/status/', api_status, name='api-status'),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)