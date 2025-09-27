from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    EXPERIENCE_LEVELS = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True,
        help_text="Formato: '+999999999'. Hasta 15 dígitos."
    )
    location = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVELS,
        default='beginner'
    )
    available_space = models.PositiveIntegerField(
        help_text="Espacio disponible en metros cuadrados",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} - {self.experience_level}"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
