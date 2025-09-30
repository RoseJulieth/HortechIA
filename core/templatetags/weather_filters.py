from django import template

register = template.Library()

@register.filter
def weather_icon_class(icon):
    """
    Convierte iconos del clima a clases de Font Awesome
    """
    icon_map = {
        'sunny': 'fas fa-sun text-warning',
        'clear': 'fas fa-sun text-warning',
        'partly_cloudy': 'fas fa-cloud-sun text-info',
        'cloudy': 'fas fa-cloud text-secondary',
        'rainy': 'fas fa-cloud-rain text-primary',
        'stormy': 'fas fa-bolt text-danger',
        'snow': 'fas fa-snowflake text-light'
    }
    
    return icon_map.get(icon, 'fas fa-cloud text-secondary')