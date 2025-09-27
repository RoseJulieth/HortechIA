from rest_framework import serializers
from .models import Garden, Plant, CultivationPlan
from django.contrib.auth import get_user_model

User = get_user_model()

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

class GardenSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Garden
        fields = ['id', 'name', 'location', 'size_m2', 'soil_type', 
                 'sun_exposure', 'has_irrigation', 'notes', 'owner_name', 'created_at']
        read_only_fields = ['id', 'created_at', 'owner_name']

class CultivationPlanSerializer(serializers.ModelSerializer):
    garden_name = serializers.CharField(source='garden.name', read_only=True)
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    plant_difficulty = serializers.CharField(source='plant.difficulty', read_only=True)
    
    class Meta:
        model = CultivationPlan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'location', 'experience_level', 
                 'available_space', 'phone_number']
        read_only_fields = ['id']