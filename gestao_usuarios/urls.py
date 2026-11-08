from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_usuarios, name='listar_usuarios'),
    path('novo/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path(
        'editar/<int:usuario_id>/',
        views.editar_usuario,
        name='editar_usuario'
    ),
    path(
        'alternar-status/<int:usuario_id>/',
        views.alternar_status_usuario,
        name='alternar_status_usuario'
    ),
]
