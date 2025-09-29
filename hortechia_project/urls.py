from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from gardens.views import GardenViewSet, PlantViewSet, CultivationPlanViewSet
from ai_recommendations.views import AIRecommendationViewSet
from core.views import (
    home, api_status, login_view, logout_view, register_view, dashboard, 
    gardens_list, garden_detail, create_garden, plants_catalog, 
    plant_detail, ai_recommendations, create_cultivation_plan
)

# Router para API REST
router = DefaultRouter()
router.register(r'gardens', GardenViewSet, basename='garden')
router.register(r'plants', PlantViewSet, basename='plant')
router.register(r'cultivation-plans', CultivationPlanViewSet, basename='cultivation-plan')
router.register(r'ai-recommendations', AIRecommendationViewSet, basename='ai-recommendation')

urlpatterns = [
    # Frontend páginas web
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # Jardines
    path('jardines/', gardens_list, name='gardens_list'),
    path('jardines/<int:garden_id>/', garden_detail, name='garden_detail'),
    path('jardines/crear/', create_garden, name='create_garden'),
    
    # Plantas
    path('plantas/', plants_catalog, name='plants_catalog'),
    path('plantas/<int:plant_id>/', plant_detail, name='plant_detail'),
    
    # IA y Planes
    path('jardines/<int:garden_id>/recomendaciones/', ai_recommendations, name='ai_recommendations'),
    path('jardines/<int:garden_id>/crear-plan/', create_cultivation_plan, name='create_cultivation_plan'),
    
    # Administración
    path('admin/', admin.site.urls),
    
    # API REST
    path('api/v1/', include(router.urls)),
    path('api/v1/status/', api_status, name='api-status'),
    
    # Autenticación API
    path('api-auth/', include('rest_framework.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)