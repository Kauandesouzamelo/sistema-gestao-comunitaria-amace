from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),
    path('novo/', views.cadastrar_produto, name='cadastrar_produto'),
    path(
        'movimentar/',
        views.registrar_movimentacao,
        name='registrar_movimentacao'
    ),
    path(
        'historico/',
        views.historico_movimentacoes,
        name='historico_movimentacoes'
    ),
    path(
        'relatorios/',
        views.relatorios,
        name='relatorios'
    ),
]
