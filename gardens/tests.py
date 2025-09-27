from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Garden, Plant, CultivationPlan

User = get_user_model()

class SecurityTestCase(APITestCase):
    """Tests de seguridad OWASP"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com', 
            password='otherpass123'
        )
        
    def test_authentication_required(self):
        """Test que endpoints requieren autenticación"""
        response = self.client.get('/api/v1/gardens/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_sql_injection_prevention(self):
        """Test prevención de SQL injection"""
        self.client.force_authenticate(user=self.user)
        
        # Intento de SQL injection en búsqueda
        malicious_input = "'; DROP TABLE gardens_plant; --"
        response = self.client.get(f'/api/v1/plants/by_difficulty/?level={malicious_input}')
        
        # Debe retornar error de validación, no crash
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verificar que la tabla sigue existiendo
        self.assertTrue(Plant.objects.count() >= 0)
        
    def test_access_control(self):
        """Test que usuarios solo acceden a sus datos"""
        self.client.force_authenticate(user=self.user)
        
        # Crear jardín para otro usuario
        other_garden = Garden.objects.create(
            owner=self.other_user,
            name='Jardín Ajeno',
            location='Lugar secreto',
            size_m2=5.0,
            soil_type='sandy',
            sun_exposure='shade'
        )
        
        # Usuario no debe ver jardín de otro
        response = self.client.get('/api/v1/gardens/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        garden_ids = [g['id'] for g in response.data]
        self.assertNotIn(other_garden.id, garden_ids)
        
    def test_input_validation(self):
        """Test validación de entrada"""
        self.client.force_authenticate(user=self.user)
        
        # Datos inválidos para crear jardín
        invalid_data = {
            'name': '',  # Nombre vacío
            'size_m2': -5,  # Tamaño negativo
            'soil_type': 'invalid_type',  # Tipo inválido
        }
        
        response = self.client.post('/api/v1/gardens/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PlantModelTest(TestCase):
    """Tests del modelo Plant"""
    
    def test_plant_creation(self):
        """Test creación de planta"""
        plant = Plant.objects.create(
            name='Test Plant',
            description='Una planta de prueba',
            difficulty='easy',
            planting_season='spring',
            harvest_time_days=30,
            space_required=1.0,
            water_frequency=3
        )
        
        self.assertEqual(plant.name, 'Test Plant')
        self.assertEqual(plant.difficulty, 'easy')
        self.assertTrue(plant.harvest_time_days > 0)

class AIRecommendationTest(APITestCase):
    """Tests del servicio de IA"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='aiuser',
            email='ai@test.com',
            password='aipass123',
            experience_level='beginner'
        )
        
        self.garden = Garden.objects.create(
            owner=self.user,
            name='Test Garden',
            location='Test Location',
            size_m2=5.0,
            soil_type='loamy',
            sun_exposure='full_sun'
        )
        
        Plant.objects.create(
            name='Easy Plant',
            description='Test plant',
            difficulty='easy',
            planting_season='spring',
            harvest_time_days=30,
            space_required=1.0,
            water_frequency=2
        )
    
    def test_ai_recommendations_generation(self):
        """Test generación de recomendaciones IA"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            '/api/v1/ai-recommendations/generate_recommendations/',
            {'garden_id': self.garden.id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('recommendations', response.data)
        self.assertIn('garden', response.data)
        
    def test_ai_rate_limiting(self):
        """Test rate limiting en IA"""
        self.client.force_authenticate(user=self.user)
        
        # Hacer múltiples requests rápidos
        for _ in range(12):  # Límite es 10/minuto
            response = self.client.post(
                '/api/v1/ai-recommendations/generate_recommendations/',
                {'garden_id': self.garden.id}
            )
        
        # El último debe ser rate limited
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)