#!/usr/bin/env python
"""
Script para inicializar datos de prueba en HortechIA
Ejecutar con: python init_data.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hortechia_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from gardens.models import Plant, Garden, CultivationPlan
from datetime import datetime, timedelta

User = get_user_model()

def create_demo_user():
    """Crear usuario demo"""
    demo_user, created = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@hortechia.com',
            'experience_level': 'beginner',
            'location': 'Santiago, Chile',
            'available_space': 10,
            'first_name': 'Usuario',
            'last_name': 'Demo'
        }
    )
    
    if created:
        demo_user.set_password('demo123')
        demo_user.save()
        print("✓ Usuario demo creado: demo@hortechia.com / demo123")
    else:
        print("ℹ Usuario demo ya existe")
    
    return demo_user

def create_sample_plants():
    """Crear plantas de ejemplo"""
    plants_data = [
        {
            'name': 'Lechuga',
            'scientific_name': 'Lactuca sativa',
            'description': 'Hortaliza de hoja verde, fácil de cultivar y de crecimiento rápido. Ideal para principiantes.',
            'difficulty': 'easy',
            'planting_season': 'all_year',
            'harvest_time_days': 45,
            'space_required': 0.25,
            'water_frequency': 2
        },
        {
            'name': 'Tomate Cherry',
            'scientific_name': 'Solanum lycopersicum var. cerasiforme',
            'description': 'Variedad pequeña de tomate, perfecta para cultivos en macetas y espacios reducidos.',
            'difficulty': 'easy',
            'planting_season': 'spring',
            'harvest_time_days': 70,
            'space_required': 1.0,
            'water_frequency': 3
        },
        {
            'name': 'Albahaca',
            'scientific_name': 'Ocimum basilicum',
            'description': 'Hierba aromática muy útil en la cocina. Requiere sol directo y riego moderado.',
            'difficulty': 'easy',
            'planting_season': 'spring',
            'harvest_time_days': 30,
            'space_required': 0.15,
            'water_frequency': 2
        },
        {
            'name': 'Perejil',
            'scientific_name': 'Petroselinum crispum',
            'description': 'Hierba culinaria resistente, crece en diversas condiciones.',
            'difficulty': 'easy',
            'planting_season': 'all_year',
            'harvest_time_days': 25,
            'space_required': 0.1,
            'water_frequency': 3
        },
        {
            'name': 'Cilantro',
            'scientific_name': 'Coriandrum sativum',
            'description': 'Hierba aromática esencial en la cocina latinoamericana.',
            'difficulty': 'easy',
            'planting_season': 'spring',
            'harvest_time_days': 40,
            'space_required': 0.15,
            'water_frequency': 3
        }
    ]

    plants_created = 0
    for plant_data in plants_data:
        plant, created = Plant.objects.get_or_create(
            name=plant_data['name'],
            defaults=plant_data
        )
        if created:
            plants_created += 1
            print(f"✓ Planta creada: {plant.name}")

    print(f"✓ {plants_created} plantas nuevas agregadas")
    return Plant.objects.all()

def create_sample_garden(user):
    """Crear jardín de ejemplo"""
    garden, created = Garden.objects.get_or_create(
        owner=user,
        name='Mi Primer Huerto',
        defaults={
            'location': 'Patio trasero, Santiago',
            'size_m2': 8.0,
            'soil_type': 'loamy',
            'sun_exposure': 'full_sun',
            'has_irrigation': False,
            'notes': 'Jardín de prueba para principiantes. Orientación norte, buen drenaje.'
        }
    )

    if created:
        print(f"✓ Jardín creado: {garden.name}")
    else:
        print("ℹ Jardín ya existe")
    
    return garden

def main():
    """Función principal"""
    print("🌱 Iniciando configuración de datos de prueba...")
    
    # Crear usuario demo
    demo_user = create_demo_user()
    
    # Crear plantas
    plants = create_sample_plants()
    
    # Crear jardín de ejemplo
    garden = create_sample_garden(demo_user)
    
    # Estadísticas finales
    total_users = User.objects.count()
    total_plants = Plant.objects.count()
    total_gardens = Garden.objects.count()

    print("\n🎉 Configuración completada exitosamente!")
    print(f"📊 Estadísticas:")
    print(f"   - Usuarios: {total_users}")
    print(f"   - Plantas: {total_plants}")
    print(f"   - Jardines: {total_gardens}")
    print("\n🔑 Credenciales de acceso:")
    print(f"   Demo: demo@hortechia.com / demo123")
    if User.objects.filter(is_superuser=True).exists():
        print(f"   Admin: (usa las credenciales que creaste con createsuperuser)")

if __name__ == '__main__':
    main()