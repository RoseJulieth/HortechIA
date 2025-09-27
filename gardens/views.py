from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .models import Garden, Plant, CultivationPlan
from .serializers import GardenSerializer, PlantSerializer, CultivationPlanSerializer
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo al dueño editar sus objetos
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

@method_decorator(ratelimit(key='user', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='user', rate='20/h', method='POST'), name='create')
class GardenViewSet(viewsets.ModelViewSet):
    serializer_class = GardenSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Filtrar solo jardines del usuario autenticado
        return Garden.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Asignar automáticamente el usuario como propietario
        serializer.save(owner=self.request.user)
        logger.info(f"Garden created by user {self.request.user.id}")

@method_decorator(ratelimit(key='ip', rate='200/h', method='GET'), name='list')
class PlantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        difficulty = request.query_params.get('level', 'easy')
        # Validación de entrada para prevenir injection
        if difficulty not in ['easy', 'medium', 'hard']:
            return Response(
                {'error': 'Invalid difficulty level'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plants = Plant.objects.filter(difficulty=difficulty)
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)

@method_decorator(ratelimit(key='user', rate='50/h', method='POST'), name='create')
class CultivationPlanViewSet(viewsets.ModelViewSet):
    serializer_class = CultivationPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CultivationPlan.objects.filter(garden__owner=self.request.user)
    
    def perform_create(self, serializer):
        garden = serializer.validated_data['garden']
        # Verificar que el jardín pertenece al usuario
        if garden.owner != self.request.user:
            raise PermissionError("No tienes permiso para este jardín")
        serializer.save()