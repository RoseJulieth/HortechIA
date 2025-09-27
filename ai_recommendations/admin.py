from django.contrib import admin
from .models import AIRecommendation, UserFeedback

@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'recommendation_type', 'confidence_score', 'status', 'created_at')
    list_filter = ('recommendation_type', 'status', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'recommendation__title')