from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions

# Nuevos imports añadidos
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Vista general e información de la API
schema_view = get_schema_view(
   openapi.Info(
      title="Todo API",
      default_version='v1',
      description="Proyecto TODO API de Silabuz",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('pagos.urls')),

    path('users/', include('users.urls')),
    # Nuevas rutas añadidas
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('users/', include('users.urls')),
#     path('', include('pagos.urls')),
# ]
