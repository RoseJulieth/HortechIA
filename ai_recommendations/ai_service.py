import random
from datetime import datetime, timedelta
from typing import Dict, List
from gardens.models import Plant, Garden
from django.contrib.auth import get_user_model

User = get_user_model()

class AIRecommendationService:
    """
    Servicio simulado de IA para generar recomendaciones
    En producción se conectaría a modelos ML reales
    """
    
    def __init__(self):
        self.confidence_threshold = 0.7
    
    def generate_plant_recommendations(self, user: User, garden: Garden) -> List[Dict]:
        """
        Genera recomendaciones de plantas basado en perfil de usuario y jardín
        """
        recommendations = []
        
        # Filtrar plantas por experiencia del usuario
        difficulty_map = {
            'beginner': ['easy'],
            'intermediate': ['easy', 'medium'],
            'advanced': ['easy', 'medium', 'hard']
        }
        
        suitable_difficulties = difficulty_map.get(user.experience_level, ['easy'])
        suitable_plants = Plant.objects.filter(difficulty__in=suitable_difficulties)
        
        # Filtrar por espacio disponible
        if garden.size_m2:
            suitable_plants = suitable_plants.filter(space_required__lte=garden.size_m2)
        
        # Generar recomendaciones con scores
        for plant in suitable_plants[:5]:  # Top 5 recomendaciones
            confidence = self._calculate_confidence(user, garden, plant)
            
            if confidence >= self.confidence_threshold:
                recommendations.append({
                    'plant_id': plant.id,
                    'plant_name': plant.name,
                    'confidence_score': round(confidence, 2),
                    'reasons': self._generate_reasons(user, garden, plant),
                    'estimated_harvest_date': self._calculate_harvest_date(plant),
                })
        
        return sorted(recommendations, key=lambda x: x['confidence_score'], reverse=True)
    
    def _calculate_confidence(self, user: User, garden: Garden, plant: Plant) -> float:
        """
        Calcula score de confianza basado en múltiples factores
        """
        confidence = 0.5  # Base confidence
        
        # Factor experiencia
        experience_boost = {
            'beginner': 0.1,
            'intermediate': 0.2,
            'advanced': 0.3
        }
        confidence += experience_boost.get(user.experience_level, 0.1)
        
        # Factor dificultad de planta
        if plant.difficulty == 'easy':
            confidence += 0.2
        elif plant.difficulty == 'medium':
            confidence += 0.1
        
        # Factor espacio
        if garden.size_m2 and plant.space_required <= garden.size_m2 * 0.5:
            confidence += 0.15
        
        # Factor exposición solar
        if garden.sun_exposure == 'full_sun':
            confidence += 0.1
        
        # Añadir algo de randomness para simular ML
        confidence += random.uniform(-0.1, 0.1)
        
        return min(confidence, 1.0)
    
    def _generate_reasons(self, user: User, garden: Garden, plant: Plant) -> List[str]:
        """
        Genera razones para la recomendación
        """
        reasons = []
        
        if plant.difficulty == 'easy' and user.experience_level == 'beginner':
            reasons.append("Ideal para principiantes")
        
        if plant.space_required <= garden.size_m2:
            reasons.append(f"Se adapta al espacio disponible ({garden.size_m2}m²)")
        
        if garden.has_irrigation and plant.water_frequency <= 3:
            reasons.append("Compatible con tu sistema de riego")
        
        reasons.append(f"Cosecha en {plant.harvest_time_days} días")
        
        return reasons
    
    def _calculate_harvest_date(self, plant: Plant) -> str:
        """
        Calcula fecha estimada de cosecha
        """
        harvest_date = datetime.now() + timedelta(days=plant.harvest_time_days)
        return harvest_date.strftime("%Y-%m-%d")