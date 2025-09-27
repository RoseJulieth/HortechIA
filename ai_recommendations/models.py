from django.db import models
from django.contrib.auth import get_user_model
from gardens.models import CultivationPlan
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class AIRecommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ('watering', 'Riego'),
        ('fertilizing', 'Fertilización'),
        ('pruning', 'Poda'),
        ('pest_control', 'Control de plagas'),
        ('harvesting', 'Cosecha'),
        ('general', 'General'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('applied', 'Aplicada'),
        ('dismissed', 'Descartada'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cultivation_plan = models.ForeignKey(
        CultivationPlan, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.confidence_score:.2f}"

class UserFeedback(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(AIRecommendation, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback: {self.rating}/5 - {self.recommendation.title}"