from django.contrib import admin
from .models import Plant, Garden, CultivationPlan

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'difficulty', 'planting_season', 'harvest_time_days')
    list_filter = ('difficulty', 'planting_season')
    search_fields = ('name', 'scientific_name')
    ordering = ('name',)

@admin.register(Garden) 
class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'size_m2', 'soil_type', 'sun_exposure', 'created_at')
    list_filter = ('soil_type', 'sun_exposure', 'has_irrigation')
    search_fields = ('name', 'owner__username', 'location')
    raw_id_fields = ('owner',)

@admin.register(CultivationPlan)
class CultivationPlanAdmin(admin.ModelAdmin):
    list_display = ('garden', 'plant', 'status', 'planting_date', 'expected_harvest_date')
    list_filter = ('status', 'planting_date')
    search_fields = ('garden__name', 'plant__name')
    raw_id_fields = ('garden', 'plant')
    date_hierarchy = 'planting_date'