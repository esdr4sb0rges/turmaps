# Importa a função path para definir rotas
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# Importa as views do app
from . import views

urlpatterns = [
    # --- Rotas para as páginas públicas do site ---
    # Página inicial do site.
    path('', views.index, name='index'),
    # Página que lista todas as atrações para os visitantes.
    path('atracoes/', views.atracoes, name='atracoes'),
    # Página do mapa interativo.
    path('mapa/', views.mapa, name='mapa'),
    # Página "Sobre".
    path('sobre/', views.sobre, name='sobre'),
    # Página de "Contato".
    path('contato/', views.contato, name='contato'),

    # --- Rotas de Autenticação e Gerenciamento de Usuário ---
    # Página de cadastro de novos usuários.
    path('cadastro/', views.cadastro, name='cadastro'),
    # Página de login.
    path('login/', views.login, name='login'),
    # Rota para executar o logout do usuário.
    path('logout/', views.logout_view, name='logout'),

    # --- Rotas para o CRUD de Atrações (requer login de staff) ---
    # Página de listagem de atrações para administradores.
    path('atracoes/admin/', views.atracoes_admin_index, name='atracoes_admin_index'),
    # Página para criar uma nova atração.
    path('atracoes/nova/', views.atracoes_create, name='atracoes_create'),
    # Página para editar uma atração existente, identificada por seu ID.
    path('atracoes/editar/<int:id>/', views.atracoes_edit, name='atracoes_edit'),
    # Rota para deletar uma atração, identificada por seu ID.
    path('atracoes/deletar/<int:id>/', views.atracoes_delete, name='atracoes_delete'),

    # --- Rotas para o CRUD de Usuários (requer login de staff) ---
    # Página de listagem de todos os usuários.
    path('usuarios/', views.usuarios_index, name='usuarios_index'),
    # Página para criar um novo usuário (pelo admin).
    path('usuarios/criar/', views.usuarios_create, name='usuarios_create'),
    # Página para editar um usuário existente, identificado por seu ID.
    path('usuarios/editar/<int:id>/', views.usuarios_edit, name='usuarios_edit'),
    # Rota para deletar um usuário, identificado por seu ID.
    path('usuarios/deletar/<int:id>/', views.usuarios_delete, name='usuarios_delete'),
]

# Configuração para servir arquivos de mídia (uploads) em ambiente de desenvolvimento.
# Em produção, o servidor web (como Nginx ou Apache) deve ser configurado para isso.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)