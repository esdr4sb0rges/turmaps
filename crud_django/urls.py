"""
URL configuration for crud_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Importa o módulo admin do Django
from django.contrib import admin
#Importa a função path para criar rotas e include para incluir rotas de apps
from django.urls import path, include
# Define as rotas do projeto
urlpatterns = [
    #Rota para acessar o painel administrativo padrão do Django
    path('admin/', admin.site.urls),
    # Inclui as rotas do aplicativo crud_app
    # A URL raiz ('') será redirecionada para o arquivo urls.py do crud_app
    path('', include('crud_app.urls')),
]
