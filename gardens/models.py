from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Plant(models.Model):
    DIFFICULTY_LEVELS = [
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil'),
    ]
    
    SEASONS = [
        ('spring', 'Primavera'),
        ('summer', 'Verano'),
        ('autumn', 'Otoño'),
        ('winter', 'Invierno'),
        ('all_year', 'Todo el año'),
    ]
    
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    planting_season = models.CharField(max_length=20, choices=SEASONS)
    harvest_time_days = models.PositiveIntegerField(
        help_text="Días desde siembra hasta cosecha"
    )
    space_required = models.FloatField(
        help_text="Espacio requerido en metros cuadrados"
    )
    water_frequency = models.PositiveIntegerField(
        help_text="Frecuencia de riego en días"
    )
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.difficulty})"

class Garden(models.Model):
    SOIL_TYPES = [
        ('sandy', 'Arenoso'),
        ('clay', 'Arcilloso'),
        ('loamy', 'Franco'),
        ('rocky', 'Rocoso'),
    ]
    
    EXPOSURE_TYPES = [
        ('full_sun', 'Sol directo'),
        ('partial_sun', 'Sol parcial'),
        ('shade', 'Sombra'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gardens')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    size_m2 = models.FloatField(validators=[MinValueValidator(0.1)])
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    sun_exposure = models.CharField(max_length=20, choices=EXPOSURE_TYPES)
    has_irrigation = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.owner.username}"

class CultivationPlan(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planificado'),
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]
    
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    actual_harvest_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    ai_recommendations = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.garden.name} - {self.plant.name} ({self.status})"