from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.db import models
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
        # Permisos de lectura para cualquier request,
        # Permisos de escritura solo para el dueño del objeto
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

@method_decorator(ratelimit(key='user', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='user', rate='20/h', method='POST'), name='create')
class GardenViewSet(viewsets.ModelViewSet):
    serializer_class = GardenSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # CRÍTICO: Filtrar solo jardines del usuario autenticado
        return Garden.objects.filter(owner=self.request.user).select_related('owner')
    
    def perform_create(self, serializer):
        # CRÍTICO: Asignar automáticamente el usuario como propietario
        serializer.save(owner=self.request.user)
        logger.info(f"Garden created by user {self.request.user.id}")

@method_decorator(ratelimit(key='ip', rate='200/h', method='GET'), name='list')
class PlantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Filtrar plantas por nivel de dificultad"""
        difficulty = request.query_params.get('level', 'easy')
        
        # Validación estricta de entrada para prevenir injection
        valid_difficulties = ['easy', 'medium', 'hard']
        if difficulty not in valid_difficulties:
            return Response(
                {'error': 'Nivel de dificultad inválido. Opciones: easy, medium, hard'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plants = Plant.objects.filter(difficulty=difficulty)
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Búsqueda segura de plantas"""
        query = request.query_params.get('q', '').strip()
        
        # Validación de entrada
        if len(query) < 2:
            return Response(
                {'error': 'La búsqueda debe tener al menos 2 caracteres'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Sanitización básica
        if not query.replace(' ', '').isalnum():
            return Response(
                {'error': 'La búsqueda solo puede contener letras, números y espacios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Búsqueda segura usando ORM (previene SQL injection)
        plants = Plant.objects.filter(
            models.Q(name__icontains=query) | 
            models.Q(scientific_name__icontains=query)
        )[:20]  # Limitar resultados
        
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)

@method_decorator(ratelimit(key='user', rate='50/h', method='POST'), name='create')
class CultivationPlanViewSet(viewsets.ModelViewSet):
    serializer_class = CultivationPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Solo planes de jardines del usuario autenticado
        return CultivationPlan.objects.filter(garden__owner=self.request.user)
    
    def perform_create(self, serializer):
        garden = serializer.validated_data['garden']
        # Verificar que el jardín pertenece al usuario (control de acceso)
        if garden.owner != self.request.user:
            raise permissions.PermissionDenied("No tienes permiso para este jardín")
        serializer.save()
        logger.info(f"Cultivation plan created by user {self.request.user.id}")
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Actualizar estado del plan de cultivo"""
        plan = self.get_object()
        new_status = request.data.get('status')
        
        # Validación de estado
        valid_statuses = ['planned', 'active', 'completed', 'failed']
        if new_status not in valid_statuses:
            return Response(
                {'error': 'Estado inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.status = new_status
        plan.save()
        
        serializer = self.get_serializer(plan)
        return Response(serializer.data)