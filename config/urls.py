from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('beneficiarios/', include('beneficiarios.urls')),
    path('estoque/', include('controle_estoque.urls')),
    path('beneficiarios/', include('beneficiarios.urls')),
    path('estoque/', include('controle_estoque.urls')),
    path('contas/', include('django.contrib.auth.urls')),
    path('usuarios/', include('gestao_usuarios.urls')),
]
