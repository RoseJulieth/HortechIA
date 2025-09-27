from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .ai_service import AIRecommendationService
from gardens.models import Garden
import logging

logger = logging.getLogger(__name__)

@method_decorator(ratelimit(key='user', rate='10/m', method='POST'), name='generate_recommendations')
class AIRecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai_service = AIRecommendationService()
    
    @action(detail=False, methods=['post'])
    def generate_recommendations(self, request):
        """
        Genera recomendaciones de plantas usando IA
        """
        try:
            garden_id = request.data.get('garden_id')
            
            if not garden_id:
                return Response(
                    {'error': 'garden_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar que el jardín pertenece al usuario
            try:
                garden = Garden.objects.get(id=garden_id, owner=request.user)
            except Garden.DoesNotExist:
                return Response(
                    {'error': 'Jardín no encontrado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Generar recomendaciones
            recommendations = self.ai_service.generate_plant_recommendations(
                request.user, garden
            )
            
            logger.info(f"AI recommendations generated for user {request.user.id}")
            
            return Response({
                'garden': garden.name,
                'recommendations': recommendations,
                'generated_at': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )