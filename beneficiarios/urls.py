from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_beneficiarios, name="listar_beneficiarios"),
    path("novo/", views.cadastrar_beneficiario, name="cadastrar_beneficiario"),
    path("editar/<int:pk>/", views.editar_beneficiario,
         name="editar_beneficiario"),
    path("excluir/<int:pk>/", views.excluir_beneficiario,
         name="excluir_beneficiario"),
]
