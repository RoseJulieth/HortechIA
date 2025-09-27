from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gardens.models import Plant, Garden, CultivationPlan
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga datos de prueba para HortechIA'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos de prueba...')
        
        # Crear usuario de prueba
        if not User.objects.filter(username='demo').exists():
            user = User.objects.create_user(
                username='demo',
                email='demo@hortechia.com',
                password='demo123',
                experience_level='beginner',
                location='Santiago, Chile',
                available_space=10
            )
            self.stdout.write(f'Usuario creado: {user.username}')
        else:
            user = User.objects.get(username='demo')

        # Crear plantas de ejemplo
        plants_data = [
            {
                'name': 'Lechuga',
                'scientific_name': 'Lactuca sativa',
                'description': 'Hortaliza de hoja verde, fácil de cultivar y de crecimiento rápido.',
                'difficulty': 'easy',
                'planting_season': 'all_year',
                'harvest_time_days': 45,
                'space_required': 0.25,
                'water_frequency': 2
            },
            {
                'name': 'Tomate Cherry',
                'scientific_name': 'Solanum lycopersicum',
                'description': 'Variedad pequeña de tomate, ideal para principiantes.',
                'difficulty': 'easy',
                'planting_season': 'spring',
                'harvest_time_days': 70,
                'space_required': 1.0,
                'water_frequency': 3
            },
            {
                'name': 'Albahaca',
                'scientific_name': 'Ocimum basilicum',
                'description': 'Hierba aromática muy útil en la cocina.',
                'difficulty': 'easy',
                'planting_season': 'spring',
                'harvest_time_days': 30,
                'space_required': 0.15,
                'water_frequency': 2
            },
            {
                'name': 'Pimentón',
                'scientific_name': 'Capsicum annuum',
                'description': 'Hortaliza de fruto, requiere más cuidados.',
                'difficulty': 'medium',
                'planting_season': 'spring',
                'harvest_time_days': 90,
                'space_required': 1.5,
                'water_frequency': 3
            },
            {
                'name': 'Zanahoria',
                'scientific_name': 'Daucus carota',
                'description': 'Hortaliza de raíz, ideal para principiantes.',
                'difficulty': 'easy',
                'planting_season': 'autumn',
                'harvest_time_days': 80,
                'space_required': 0.3,
                'water_frequency': 4
            }
        ]

        for plant_data in plants_data:
            plant, created = Plant.objects.get_or_create(
                name=plant_data['name'],
                defaults=plant_data
            )
            if created:
                self.stdout.write(f'Planta creada: {plant.name}')

        # Crear jardín de ejemplo
        if not Garden.objects.filter(owner=user).exists():
            garden = Garden.objects.create(
                owner=user,
                name='Mi Primer Huerto',
                location='Patio trasero',
                size_m2=8.0,
                soil_type='loamy',
                sun_exposure='full_sun',
                has_irrigation=False,
                notes='Jardín de prueba para principiantes'
            )
            self.stdout.write(f'Jardín creado: {garden.name}')

            # Crear plan de cultivo de ejemplo
            lechuga = Plant.objects.get(name='Lechuga')
            plan = CultivationPlan.objects.create(
                garden=garden,
                plant=lechuga,
                status='active',
                planting_date=datetime.now().date(),
                expected_harvest_date=(datetime.now() + timedelta(days=lechuga.harvest_time_days)).date(),
                notes='Primer cultivo de prueba',
                ai_recommendations={
                    'watering_schedule': 'Cada 2 días por la mañana',
                    'fertilizer': 'Compost orgánico cada 2 semanas',
                    'tips': 'Proteger del sol directo en verano'
                }
            )
            self.stdout.write(f'Plan de cultivo creado: {plan}')

        self.stdout.write(
            self.style.SUCCESS('Datos de prueba cargados exitosamente!')
        )