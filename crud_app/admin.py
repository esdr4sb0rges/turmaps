from django.contrib import admin
# Importa os modelos que você criou
from .models import Cidade, Categoria, Atracao

# Cria classes de Admin para customizar a exibição

# Registra o modelo Cidade no painel de administração com configurações customizadas.
@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    # Define as colunas que serão exibidas na lista de cidades.
    list_display = ('nome',)
    # Adiciona um campo de busca que pesquisa pelo nome da cidade.
    search_fields = ('nome',)

# Registra o modelo Categoria no painel de administração.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # Define as colunas a serem exibidas na lista de categorias.
    list_display = ('nome', 'icone')
    # Adiciona um campo de busca pelo nome da categoria.
    search_fields = ('nome',)

# Registra o modelo Atracao com uma configuração mais detalhada.
@admin.register(Atracao)
class AtracaoAdmin(admin.ModelAdmin):
    # Define as colunas a serem exibidas na lista de atrações.
    list_display = ('nome', 'cidade', 'categoria', 'horario_funcionamento')
    # Adiciona uma barra lateral para filtrar as atrações por cidade e categoria.
    list_filter = ('cidade', 'categoria')
    # Adiciona um campo de busca que pesquisa no nome e na descrição da atração.
    search_fields = ('nome', 'descricao')
