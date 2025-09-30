# HortechIA MVP - Prototipo de Jardinería Inteligente

## 📋 Información del Proyecto

**Asignatura:** Ingeniería de Software  
**Evaluación:** Sumativa N°3 (40%)  
**Institución:** [Tu Universidad]  
**Desarrolladores:** Jennifer Astudillo y Carlos Velásquez  
**Fecha:** 30 de Septiembre, 2025

## 🌱 Descripción del Proyecto

HortechIA es una plataforma web de jardinería doméstica que utiliza inteligencia artificial para democratizar el conocimiento agrícola. El sistema proporciona recomendaciones personalizadas de cultivo basadas en el perfil del usuario, características del jardín, y condiciones climáticas locales.

Este prototipo funcional implementa las metodologías de desarrollo ágil (Scrum + Design Thinking) y cumple con estándares internacionales de calidad (ISO 9001, ISO/IEC 25000, ISO/IEC 12207) y seguridad (OWASP Top 10).

## ✨ Características Principales

### Funcionalidades Implementadas

- **Sistema de Autenticación Completo**
  - Registro de usuarios con validación de datos
  - Inicio de sesión seguro con autenticación por email
  - Gestión de sesiones y cierre de sesión
  - Control de acceso basado en roles

- **Gestión de Jardines**
  - Creación de jardines con información detallada
  - Especificación de tipo de suelo, exposición solar y tamaño
  - Visualización de jardines del usuario
  - Dashboard personalizado

- **Recomendaciones de IA**
  - Algoritmo de recomendación basado en múltiples variables
  - Score de confianza por cada recomendación
  - Personalización según nivel de experiencia del usuario
  - Análisis de compatibilidad planta-jardín

- **Catálogo de Plantas**
  - Base de datos de plantas con información técnica
  - Filtros por dificultad y búsqueda por nombre
  - Fichas detalladas con requerimientos de cultivo
  - Información de cosecha y cuidados

- **Planes de Cultivo**
  - Creación de planes vinculados a jardines específicos
  - Cálculo automático de fecha de cosecha
  - Seguimiento del estado de cultivos
  - Integración con recomendaciones IA

- **Panel de Administración**
  - Interfaz Django Admin completa
  - Gestión de usuarios, plantas y jardines
  - Control total del sistema

## 🛠️ Tecnologías Utilizadas

### Backend
- **Framework:** Django 4.2.7
- **API REST:** Django REST Framework 3.14.0
- **Base de Datos:** SQLite (desarrollo) / MySQL (producción)
- **Autenticación:** Django Authentication System
- **Seguridad:** django-ratelimit, CORS headers

### Frontend
- **UI Framework:** Bootstrap 5.1.3
- **Icons:** Font Awesome 6.0.0
- **Template Engine:** Django Templates
- **JavaScript:** Vanilla JS

### Herramientas de Desarrollo
- **Control de Versiones:** Git / GitHub
- **IDE:** Visual Studio Code
- **Testing:** Django TestCase, pytest
- **Gestión de Dependencias:** pip + requirements.txt

## 📁 Estructura del Proyecto

```
hortechia-mvp/
├── hortechia_project/          # Configuración principal Django
│   ├── settings.py            # Configuración del proyecto
│   ├── urls.py                # Rutas principales
│   └── wsgi.py                # WSGI para despliegue
├── core/                       # App de usuarios y autenticación
│   ├── models.py              # Modelo de usuario personalizado
│   ├── views.py               # Vistas de auth y dashboard
│   ├── admin.py               # Configuración admin
│   ├── weather_service.py     # Servicio del clima
│   ├── templatetags/          # Filtros personalizados
│   │   └── weather_filters.py # Filtros para widget del clima
│   └── tests.py               # Tests de seguridad
├── gardens/                    # App de jardines y plantas
│   ├── models.py              # Modelos Garden, Plant, CultivationPlan
│   ├── views.py               # Vistas y API REST
│   ├── serializers.py         # Serializadores API
│   ├── admin.py               # Admin de jardines
│   └── tests.py               # Tests funcionales
├── ai_recommendations/         # App de IA
│   ├── models.py              # Modelo de recomendaciones
│   ├── views.py               # API de recomendaciones
│   ├── ai_service.py          # Lógica del algoritmo IA
│   └── admin.py               # Admin de IA
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Página principal
│   ├── auth/                  # Templates de autenticación
│   ├── dashboard/             # Dashboard de usuario
│   ├── gardens/               # Gestión de jardines
│   ├── plants/                # Catálogo de plantas
│   └── ai/                    # Recomendaciones IA
├── static/                     # Archivos estáticos CSS/JS
├── media/                      # Archivos subidos por usuarios
├── requirements.txt            # Dependencias Python
├── .gitignore                 # Archivos ignorados por Git
├── .env                       # Variables de entorno (no incluido en repo)
├── db.sqlite3                 # Base de datos (desarrollo)
└── README.md                  # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/RoseJulieth/HortechIA.git
cd hortechia-mvp
```

2. **Crear entorno virtual**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Si hay error de permisos en PowerShell, ejecuta primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Esto funciona para la API del clima
```bash
SECRET_KEY=RoseJulieth
DEBUG=True
OPENWEATHER_API_KEY=eclipse1234
```
# Nota importante: El sistema funciona sin archivo .env. El widget del clima usa datos simulados por defecto. Para datos reales del clima, obtén una API key gratuita en OpenWeatherMap.

5. **Crear la carpeta static**
# Windows
mkdir static

# macOS/Linux
mkdir -p static

6. **Ejecutar migraciones de la base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```
## Se te pedirá:
- **Email: tu@email.com**
- **Nombre completo: Tu Nombre**
- **Password: (mínimo 8 caracteres)**

8. **Cargar datos de plantas de ejemplo (Opcional)**
```bash
python manage.py shell
```
# Dentro del shell ejecuta:
```bash
from gardens.models import Plant

# Crear plantas de ejemplo
Plant.objects.create(
    name="Lechuga",
    scientific_name="Lactuca sativa",
    description="Hortaliza de hoja verde, muy fácil de cultivar.",
    difficulty="easy",
    harvest_time_days=45,
    ideal_temperature_min=10,
    ideal_temperature_max=20,
    water_frequency_days=2,
    sunlight_hours_min=4,
    sunlight_hours_max=6
)

Plant.objects.create(
    name="Tomate",
    scientific_name="Solanum lycopersicum",
    description="Planta de fruto rojo, requiere cuidados moderados.",
    difficulty="medium",
    harvest_time_days=75,
    ideal_temperature_min=18,
    ideal_temperature_max=30,
    water_frequency_days=2,
    sunlight_hours_min=6,
    sunlight_hours_max=8
)

Plant.objects.create(
    name="Rúcula",
    scientific_name="Eruca vesicaria",
    description="Hoja verde picante de crecimiento rápido.",
    difficulty="easy",
    harvest_time_days=30,
    ideal_temperature_min=10,
    ideal_temperature_max=22,
    water_frequency_days=2,
    sunlight_hours_min=4,
    sunlight_hours_max=6
)

Plant.objects.create(
    name="Perejil",
    scientific_name="Petroselinum crispum",
    description="Hierba aromática fácil de cultivar.",
    difficulty="easy",
    harvest_time_days=75,
    ideal_temperature_min=15,
    ideal_temperature_max=25,
    water_frequency_days=2,
    sunlight_hours_min=4,
    sunlight_hours_max=6
)

# Salir del shell
exit()
```

9. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

10. **Acceder a la aplicación**
- Frontend: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/v1/
- API Status: http://127.0.0.1:8000/api/v1/status/
**Credenciales de Prueba**
## Después de crear tu superusuario, puedes:
## 1. Acceder al admin con las credenciales que creaste
## 2. Crear usuarios normales desde el panel admin o desde el registro público
## Ya esta creado los usuarios
## 1.ID:Admin  ----> Admin
##  Password: admin123
##  Email: admin@hortechia.com
## 2. ID:RoseJulieth  ----> User
##  Password: rose123456
##  Email: rosejulieth@email.cl

## Verificación de Instalación
Para verificar que todo funciona correctamente:
```bash
#Verificar versión de Django
python manage.py --version
# Debería mostrar: 4.2.7
```
## Verificar que no hay errores de configuración
```bash
python manage.py check
```
## Ver lista de dependencias instaladas
```bash
pip list
```
## Solución de Problemas Comunes
Error: "python no se reconoce"

## Asegúrate de tener Python instalado desde python.org
## O usa py en lugar de python

## Error al activar entorno virtual en PowerShell
```bash
bashSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
## Error: "No such file or directory: 'static'"
```bash
mkdir static
```
## Error con Pillow durante instalación
```bash
#Instala las demás dependencias primero
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1
# Luego instala Pillow
pip install Pillow
```
## Error: "OPENWEATHER_API_KEY not found"
Es normal, el sistema funciona con datos simulados por defecto
El widget del clima funcionará automáticamente con datos de prueba

## Error: "Port 8000 is already in use"
```bash
#Usa otro puerto
python manage.py runserver 8080
```

### Variables de Entorno (Opcional)
Crea un archivo `.env` en la raíz del proyecto para personalizar la configuración:
```bash
SECRET_KEY=RoseJulieth
DEBUG=True
OPENWEATHER_API_KEY=eclipse1234  # Opcional: Para datos reales del clima
```

## 👥 Uso del Sistema

### Para Usuarios Finales

1. **Registro**
   - Ir a http://127.0.0.1:8000/register/
   - Completar formulario con datos personales
   - Seleccionar nivel de experiencia

2. **Crear Jardín**
   - Acceder al dashboard
   - Clic en "Crear Jardín"
   - Especificar características del jardín

3. **Obtener Recomendaciones IA**
   - Seleccionar un jardín
   - Clic en "Generar Recomendaciones IA"
   - Revisar plantas sugeridas con score de confianza

4. **Crear Plan de Cultivo**
   - Desde recomendaciones o catálogo
   - Seleccionar planta y fecha de siembra
   - Sistema calcula automáticamente fecha de cosecha

### Para Administradores

1. **Acceso al Panel Admin**
   - http://127.0.0.1:8000/admin/
   - Usar credenciales de superusuario

2. **Gestión de Contenido**
   - Agregar/editar plantas en el catálogo
   - Moderar usuarios y jardines
   - Revisar recomendaciones generadas

## 🔒 Seguridad Implementada (OWASP Top 10)

### Controles de Seguridad

| Vulnerabilidad OWASP | Control Implementado |
|---------------------|---------------------|
| A01: Broken Access Control | Autenticación requerida, filtros por usuario, decoradores @login_required |
| A02: Cryptographic Failures | HTTPS configurado, contraseñas hasheadas (PBKDF2), cookies seguras |
| A03: Injection | Django ORM (previene SQL injection), validación de entrada |
| A04: Insecure Design | Rate limiting (django-ratelimit), validación robusta |
| A05: Security Misconfiguration | DEBUG=False en producción, headers de seguridad configurados |

### Medidas Adicionales

- **Rate Limiting:** 
  - Login: 20 intentos/hora
  - API: 100 requests/hora
  - IA: 10 requests/minuto

- **Validación de Entrada:**
  - Sanitización de datos de formularios
  - Validación de tipos de datos
  - Prevención de XSS

- **Gestión de Sesiones:**
  - Timeout automático de sesión
  - Limpieza de mensajes entre sesiones
  - Token CSRF en todos los formularios

## 🧪 Testing y Calidad

### Tests Implementados

```bash
# Ejecutar todos los tests
python manage.py test

# Tests específicos de seguridad
python manage.py test gardens.tests.SecurityTestCase

# Tests de funcionalidad
python manage.py test gardens.tests.PlantModelTest
```

### Cobertura de Tests

- **Tests de Seguridad:** SQL injection, XSS, control de acceso
- **Tests Funcionales:** CRUD de modelos, autenticación
- **Tests de API:** Endpoints REST, serialización
- **Cobertura Objetivo:** >90%

### Métricas de Calidad

- **Performance:** Tiempo de respuesta API <2s
- **Disponibilidad:** Objetivo 99.5% uptime
- **Usabilidad:** Task completion rate >95%
- **Código:** Cumplimiento PEP 8

## 📊 Cumplimiento de Evaluación

### Criterios de Evaluación Sumativa N°3

| Criterio | Puntaje | Cumplimiento |
|----------|---------|--------------|
| **3.1.1** Tendencias SaaS/IaaS/Cloud | 20 pts | ✅ Documentado en informe y README |
| **3.1.2** Confiabilidad y Ética | 20 pts | ✅ Marco ético implementado, gestión de riesgos |
| **3.1.3** Prototipo y Seguridad | 30 pts | ✅ Prototipo ejecutable, OWASP compliant |
| **3.1.4** Diagramas UML | 15 pts | ✅ Casos de uso, clases, secuencia (en informe) |
| **3.1.5** Testing y Correcciones | 15 pts | ✅ Plan de pruebas ejecutado, correcciones documentadas |

### Entregables Completados

- ✅ Prototipo funcional ejecutable
- ✅ Documento técnico (informe PDF)
- ✅ Repositorio Git con commits progresivos
- ✅ README.md con documentación completa
- ✅ Tests de seguridad y funcionalidad
- ✅ Tag de release v1.0.0

## 🌐 API Endpoints

### Autenticación
- `POST /login/` - Iniciar sesión
- `POST /register/` - Crear cuenta
- `POST /logout/` - Cerrar sesión

### Jardines (Requiere autenticación)
- `GET /api/v1/gardens/` - Listar jardines del usuario
- `POST /api/v1/gardens/` - Crear jardín
- `GET /api/v1/gardens/{id}/` - Detalle de jardín
- `PUT /api/v1/gardens/{id}/` - Actualizar jardín

### Plantas
- `GET /api/v1/plants/` - Listar plantas
- `GET /api/v1/plants/{id}/` - Detalle de planta
- `GET /api/v1/plants/by_difficulty/?level=easy` - Filtrar por dificultad

### Recomendaciones IA
- `POST /api/v1/ai-recommendations/generate_recommendations/`
  - Body: `{"garden_id": 1}`
  - Response: Lista de plantas recomendadas con scores

### Sistema
- `GET /api/v1/status/` - Estado de la API

## 🎯 Metodología de Desarrollo

### Metodología Aplicada
- **Scrum:** Sprints de 2 semanas, daily standups, retrospectivas
- **Design Thinking:** Empatizar, definir, idear, prototipar, testear
- **Integración ISO:** Procesos documentados, métricas de calidad

### Herramientas de Gestión
- **Control de versiones:** Git con commits descriptivos
- **Documentación:** Markdown, diagramas UML
- **Testing:** Django TestCase, cobertura de código

## 🔄 Próximos Pasos y Mejoras

### Funcionalidades Futuras (Roadmap)
- Integración con APIs climáticas en tiempo real
- Sistema de notificaciones push
- Modo offline para la aplicación móvil
- Reconocimiento de plagas por foto (Computer Vision)
- Comunidad de usuarios con foro
- Marketplace de productos orgánicos

### Optimizaciones Técnicas
- Migración a PostgreSQL para producción
- Implementación de cache con Redis
- CDN para archivos estáticos
- Containerización con Docker
- CI/CD con GitHub Actions

## 📞 Soporte y Contacto

### Desarrolladores
- **Jennifer Astudillo**
- **Carlos Velásquez**

### Repositorio
- GitHub: [https://github.com/RoseJulieth/HortechIA.git]

### Documentación Adicional
- Informe técnico completo (PDF)
- Diagramas UML en `/docs/`
- Plan de pruebas en `/docs/testing/`

## 📄 Licencia

Este proyecto es un trabajo académico desarrollado para la asignatura de Ingeniería de Software. Todos los derechos reservados.

## 🙏 Agradecimientos

- Profesor Marco Arévalo Zambrano por la guía durante el desarrollo
- Instituto de Investigaciones Agropecuarias (INIA) por la validación de contenido agronómico
- Comunidad de desarrolladores Django y Bootstrap

---

**Versión:** 1.0.0  
**Fecha de Release:** 30 de Septiembre, 2025  
**Estado:** Producción - Evaluación Académica
