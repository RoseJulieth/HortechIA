from django import template

register = template.Library()

@register.filter
def weather_icon(icon_name):
    """
    Convierte nombre de icono de clima a clase de Font Awesome
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
    
    return icon_map.get(icon_name, 'fas fa-cloud text-secondary')

@register.filter  
def translate_day(day_name):
    """
    Traduce nombres de días al español
    """
    translations = {
        'Monday': 'Lun',
        'Tuesday': 'Mar', 
        'Wednesday': 'Mié',
        'Thursday': 'Jue',
        'Friday': 'Vie',
        'Saturday': 'Sáb',
        'Sunday': 'Dom',
        'Mon': 'Lun',
        'Tue': 'Mar',
        'Wed': 'Mié', 
        'Thu': 'Jue',
        'Fri': 'Vie',
        'Sat': 'Sáb',
        'Sun': 'Dom'
    }
    
    return translations.get(day_name, day_name)