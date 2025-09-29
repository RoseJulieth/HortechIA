from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from gardens.models import Garden, Plant, CultivationPlan
from ai_recommendations.ai_service import AIRecommendationService
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .weather_service import WeatherService

User = get_user_model()

def home(request):
    """Vista principal del sitio"""
    context = {
        'total_plants': Plant.objects.count(),
        'total_users': User.objects.count(),
        'total_gardens': Garden.objects.count(),
    }
    return render(request, 'index.html', context)

def register_view(request):
    """Vista de registro de nuevos usuarios"""
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        experience_level = request.POST.get('experience_level')
        location = request.POST.get('location', '')
        available_space = request.POST.get('available_space')
        
        # Validaciones
        if not all([username, email, password1, password2, first_name, last_name, experience_level]):
            messages.error(request, 'Todos los campos obligatorios deben estar completos.')
            return render(request, 'auth/register.html')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'auth/register.html')
        
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'auth/register.html')
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return render(request, 'auth/register.html')
        
        try:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                experience_level=experience_level,
                location=location,
                available_space=float(available_space) if available_space else None
            )
            
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {first_name}!')
            
            # Autenticar y hacer login automáticamente
            user = authenticate(request, username=username, password=password1)
            if user:
                login(request, user)
                return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, 'Error al crear la cuenta. Intenta nuevamente.')
    
    return render(request, 'auth/register.html')

def login_view(request):
    """Vista de login personalizada"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"DEBUG: Intento de login con email: {email}")  # Debug temporal
        
        if not email or not password:
            messages.error(request, 'Email y contraseña son requeridos.')
            return render(request, 'auth/login.html')
        
        # Buscar usuario por email y autenticar
        try:
            user_obj = User.objects.get(email=email)
            print(f"DEBUG: Usuario encontrado: {user_obj.username}")  # Debug temporal
            
            user = authenticate(request, username=user_obj.username, password=password)
            print(f"DEBUG: Resultado autenticación: {user}")  # Debug temporal
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Bienvenido, {user.first_name or user.username}!')
                    print(f"DEBUG: Login exitoso para {user.username}")  # Debug temporal
                    
                    # Redirigir al dashboard o a la página solicitada
                    next_url = request.GET.get('next', 'dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Tu cuenta está desactivada.')
            else:
                messages.error(request, 'Contraseña incorrecta.')
                print("DEBUG: Contraseña incorrecta")  # Debug temporal
                
        except User.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese email.')
            print(f"DEBUG: Usuario no encontrado con email: {email}")  # Debug temporal
        except Exception as e:
            messages.error(request, 'Error al iniciar sesión. Intenta nuevamente.')
            print(f"DEBUG: Error de excepción: {e}")  # Debug temporal
    
    return render(request, 'auth/login.html')

def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('home')

@login_required
def dashboard(request):
    """Dashboard principal del usuario"""
    user_gardens = Garden.objects.filter(owner=request.user)
    recent_plants = Plant.objects.all()[:6]
    
    # Estadísticas del usuario
    total_gardens = user_gardens.count()
    active_plans = CultivationPlan.objects.filter(
        garden__owner=request.user, 
        status='active'
    ).count()
    
    # Obtener información del clima
    weather_service = WeatherService()
    user_location = request.user.location or 'Santiago, Chile'
    
    current_weather = weather_service.get_current_weather(user_location)
    weather_forecast = weather_service.get_weekly_forecast(user_location)
    gardening_tip = weather_service.get_gardening_tip(current_weather)
    
    context = {
        'user_gardens': user_gardens,
        'recent_plants': recent_plants,
        'total_gardens': total_gardens,
        'active_plans': active_plans,
        'current_weather': current_weather,
        'weather_forecast': weather_forecast,
        'gardening_tip': gardening_tip,
        'weather_service': weather_service,  # Para usar get_weather_icon_class en template
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def gardens_list(request):
    """Lista de jardines del usuario"""
    gardens = Garden.objects.filter(owner=request.user)
    paginator = Paginator(gardens, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gardens/gardens_list.html', {'page_obj': page_obj})

@login_required
def garden_detail(request, garden_id):
    """Detalle de un jardín específico"""
    garden = get_object_or_404(Garden, id=garden_id, owner=request.user)
    cultivation_plans = CultivationPlan.objects.filter(garden=garden)
    
    context = {
        'garden': garden,
        'cultivation_plans': cultivation_plans,
    }
    return render(request, 'gardens/garden_detail.html', context)

@login_required
def create_garden(request):
    """Crear nuevo jardín"""
    if request.method == 'POST':
        garden = Garden.objects.create(
            owner=request.user,
            name=request.POST.get('name'),
            location=request.POST.get('location'),
            size_m2=float(request.POST.get('size_m2')),
            soil_type=request.POST.get('soil_type'),
            sun_exposure=request.POST.get('sun_exposure'),
            has_irrigation=request.POST.get('has_irrigation') == 'on',
            notes=request.POST.get('notes', '')
        )
        messages.success(request, f'Jardín "{garden.name}" creado exitosamente!')
        return redirect('gardens_list')
    
    return render(request, 'gardens/create_garden.html')

def plants_catalog(request):
    """Catálogo público de plantas"""
    plants = Plant.objects.all()
    difficulty_filter = request.GET.get('difficulty')
    search_query = request.GET.get('search')
    
    if difficulty_filter:
        plants = plants.filter(difficulty=difficulty_filter)
    
    if search_query:
        plants = plants.filter(name__icontains=search_query)
    
    paginator = Paginator(plants, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'difficulty_filter': difficulty_filter,
        'search_query': search_query,
    }
    return render(request, 'plants/plants_catalog.html', context)

def plant_detail(request, plant_id):
    """Detalle de una planta"""
    plant = get_object_or_404(Plant, id=plant_id)
    return render(request, 'plants/plant_detail.html', {'plant': plant})

@login_required
def ai_recommendations(request, garden_id):
    """Página de recomendaciones IA"""
    garden = get_object_or_404(Garden, id=garden_id, owner=request.user)
    recommendations = []
    
    if request.method == 'POST':
        ai_service = AIRecommendationService()
        recommendations = ai_service.generate_plant_recommendations(request.user, garden)
        
        if recommendations:
            messages.success(request, f'Se generaron {len(recommendations)} recomendaciones para tu jardín!')
        else:
            messages.warning(request, 'No se encontraron recomendaciones adecuadas para tu jardín.')
    
    context = {
        'garden': garden,
        'recommendations': recommendations,
    }
    return render(request, 'ai/recommendations.html', context)

@login_required
def create_cultivation_plan(request, garden_id):
    """Crear plan de cultivo"""
    garden = get_object_or_404(Garden, id=garden_id, owner=request.user)
    
    if request.method == 'POST':
        plant_id = request.POST.get('plant_id')
        plant = get_object_or_404(Plant, id=plant_id)
        
        # Calcular fecha de cosecha automáticamente
        from datetime import datetime, timedelta
        planting_date = datetime.strptime(request.POST.get('planting_date'), '%Y-%m-%d').date()
        expected_harvest = planting_date + timedelta(days=plant.harvest_time_days)
        
        plan = CultivationPlan.objects.create(
            garden=garden,
            plant=plant,
            planting_date=planting_date,
            expected_harvest_date=expected_harvest,
            notes=request.POST.get('notes', ''),
            status='planned'
        )
        
        messages.success(request, f'Plan de cultivo para {plant.name} creado exitosamente!')
        return redirect('garden_detail', garden_id=garden.id)
    
    plants = Plant.objects.all()
    context = {
        'garden': garden,
        'plants': plants,
    }
    return render(request, 'plans/create_plan.html', context)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """Endpoint público para verificar estado de la API"""
    return Response({
        'status': 'online',
        'version': '1.0.0',
        'service': 'HortechIA API',
        'features': [
            'User Management',
            'Garden Management', 
            'AI Recommendations',
            'Plant Database',
            'Cultivation Plans'
        ],
        'security': [
            'OWASP Top 10 Compliance',
            'Rate Limiting',
            'Input Validation',
            'Authentication Required'
        ]
    })