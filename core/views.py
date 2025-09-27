from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from gardens.models import Garden, Plant
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    """Vista principal del sitio"""
    context = {
        'total_plants': Plant.objects.count(),
        'total_users': User.objects.count(),
        'total_gardens': Garden.objects.count(),
    }
    return render(request, 'index.html', context)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """Endpoint público para verificar estado de la API"""
    return Response({
        'status': 'online',
        'version': '1.0.0',
        'service': 'HortechIA API',
        'features': [
            'User Management',
            'Garden Management', 
            'AI Recommendations',
            'Plant Database',
            'Cultivation Plans'
        ],
        'security': [
            'OWASP Top 10 Compliance',
            'Rate Limiting',
            'Input Validation',
            'Authentication Required'
        ]
    })