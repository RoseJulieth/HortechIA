import requests
from datetime import datetime, timedelta
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Servicio para obtener información del clima usando OpenWeatherMap API
    """
    
    def __init__(self):
        # Obtener API key de settings
        self.api_key = settings.OPENWEATHER_API_KEY if settings.OPENWEATHER_API_KEY else "demo_key"
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, location):
        """
        Obtiene el clima actual para una ubicación
        """
        try:
            # Para el prototipo, simulamos datos realistas basados en la ubicación
            return self._get_simulated_current_weather(location)
        except Exception as e:
            logger.error(f"Error obteniendo clima actual: {e}")
            return self._get_default_weather()
    
    def get_weekly_forecast(self, location):
        """
        Obtiene el pronóstico de 7 días
        """
        try:
            # Para el prototipo, simulamos datos del pronóstico
            return self._get_simulated_forecast(location)
        except Exception as e:
            logger.error(f"Error obteniendo pronóstico: {e}")
            return self._get_default_forecast()
    
    def _get_simulated_current_weather(self, location):
        """
        Simula datos de clima actual basados en la ubicación
        """
        # Diferentes climas según la ciudad
        weather_data = {
            'santiago': {
                'temperature': 22,
                'description': 'Parcialmente nublado',
                'humidity': 65,
                'wind_speed': 8,
                'icon': 'partly_cloudy'
            },
            'valparaiso': {
                'temperature': 18,
                'description': 'Nublado',
                'humidity': 78,
                'wind_speed': 12,
                'icon': 'cloudy'
            },
            'la serena': {
                'temperature': 25,
                'description': 'Soleado',
                'humidity': 45,
                'wind_speed': 6,
                'icon': 'sunny'
            }
        }
        
        # Buscar coincidencia en la ubicación
        location_lower = location.lower()
        for city, data in weather_data.items():
            if city in location_lower:
                return {
                    'location': location,
                    'temperature': data['temperature'],
                    'description': data['description'],
                    'humidity': data['humidity'],
                    'wind_speed': data['wind_speed'],
                    'icon': data['icon'],
                    'last_updated': datetime.now().strftime("%H:%M")
                }
        
        # Default para ubicaciones no específicas
        return {
            'location': location,
            'temperature': 20,
            'description': 'Clima templado',
            'humidity': 60,
            'wind_speed': 7,
            'icon': 'partly_cloudy',
            'last_updated': datetime.now().strftime("%H:%M")
        }
    
    def _get_simulated_forecast(self, location):
        """
        Simula pronóstico de 7 días
        """
        base_temp = 20
        location_lower = location.lower()
        
        # Ajustar temperatura base según ubicación
        if 'santiago' in location_lower:
            base_temp = 22
        elif 'valparaiso' in location_lower:
            base_temp = 18
        elif 'la serena' in location_lower:
            base_temp = 25
        
        forecast = []
        weather_patterns = [
            {'desc': 'Soleado', 'icon': 'sunny'},
            {'desc': 'Parcialmente nublado', 'icon': 'partly_cloudy'},
            {'desc': 'Nublado', 'icon': 'cloudy'},
            {'desc': 'Lluvia ligera', 'icon': 'rainy'},
            {'desc': 'Despejado', 'icon': 'clear'},
        ]
        
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            pattern = weather_patterns[i % len(weather_patterns)]
            
            # Variar temperatura
            temp_variation = (-3, -1, 0, 1, 2, -2, 1)[i]
            
            forecast.append({
                'date': date.strftime("%Y-%m-%d"),
                'day_name': date.strftime("%A"),
                'day_short': date.strftime("%a"),
                'max_temp': base_temp + temp_variation + 3,
                'min_temp': base_temp + temp_variation - 2,
                'description': pattern['desc'],
                'icon': pattern['icon']
            })
        
        return forecast
    
    def _get_default_weather(self):
        """
        Datos de clima por defecto en caso de error
        """
        return {
            'location': 'Ubicación no disponible',
            'temperature': 20,
            'description': 'Clima templado',
            'humidity': 60,
            'wind_speed': 7,
            'icon': 'partly_cloudy',
            'last_updated': datetime.now().strftime("%H:%M")
        }
    
    def _get_default_forecast(self):
        """
        Pronóstico por defecto en caso de error
        """
        forecast = []
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            forecast.append({
                'date': date.strftime("%Y-%m-%d"),
                'day_name': date.strftime("%A"),
                'day_short': date.strftime("%a"),
                'max_temp': 22 + (i % 3),
                'min_temp': 15 + (i % 2),
                'description': 'Templado',
                'icon': 'partly_cloudy'
            })
        
        return forecast
    
    def get_weather_icon_class(self, icon):
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
    
    def get_gardening_tip(self, weather_data):
        """
        Genera consejos de jardinería basados en el clima
        """
        temp = weather_data.get('temperature', 20)
        description = weather_data.get('description', '').lower()
        
        if 'lluvia' in description or 'rain' in description:
            return "Día perfecto para que las plantas se hidraten naturalmente. Evita regar."
        elif temp > 28:
            return "Día caluroso. Riega temprano en la mañana o al atardecer."
        elif temp < 10:
            return "Protege plantas sensibles al frío. Considera riego reducido."
        elif 'sol' in description or 'sunny' in description:
            return "Excelente día para actividades de jardinería al aire libre."
        else:
            return "Buen día para cuidados generales del jardín."