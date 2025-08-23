# frota/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rotas Públicas
    path('', views.index, name='index'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='frota/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    # Painel Admin
    path('painel/', views.admin_panel, name='admin_panel'),
    
    # Gerenciamento de Departamentos
    path('painel/departamentos/', views.gerenciar_departamentos, name='gerenciar_departamentos'),
    path('painel/departamentos/editar/<int:id>/', views.editar_departamento, name='editar_departamento'),
    path('painel/departamentos/excluir/<int:id>/', views.excluir_departamento, name='excluir_departamento'),

    # Gerenciamento de Veículos
    path('painel/veiculos/', views.gerenciar_veiculos, name='gerenciar_veiculos'),
    path('painel/veiculos/editar/<int:id>/', views.editar_veiculo, name='editar_veiculo'),
    path('painel/veiculos/excluir/<int:id>/', views.excluir_veiculo, name='excluir_veiculo'),

    # Ações de Status do Veículo
    path('painel/veiculos/manutencao/<int:id>/', views.gerenciar_manutencao, name='gerenciar_manutencao'),
    path('painel/veiculos/manutencao/concluir/<int:id>/', views.concluir_manutencao, name='concluir_manutencao'),
    path('painel/veiculos/indisponivel/<int:id>/', views.gerenciar_indisponibilidade, name='gerenciar_indisponibilidade'),
    path('painel/veiculos/indisponivel/concluir/<int:id>/', views.tornar_disponivel, name='tornar_disponivel'),

    path('painel/modelos/', views.gerenciar_modelos, name='gerenciar_modelos'),
    path('painel/modelos/editar/<int:id>/', views.editar_modelo, name='editar_modelo'),
    path('painel/modelos/excluir/<int:id>/', views.excluir_modelo, name='excluir_modelo'),

]