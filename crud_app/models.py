# Importa o módulo de modelos do Django
from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings
import os

# Função customizada para definir o caminho de upload da imagem
# Ela cria um caminho único para a imagem de cada atração, usando o ID da atração.
# Ex: 'atracoes/img/5/nome_do_arquivo.jpg'
def atracao_image_path(instance, filename):
    return f'atracoes/img/{instance.pk}/{filename}'

# Modelo para representar as cidades
class Cidade(models.Model):
    # Campo para o nome da cidade, com um máximo de 100 caracteres e deve ser único.
    nome = models.CharField(max_length=100, unique=True)

    # Define a representação em string do objeto, que será o nome da cidade.
    def __str__(self):
        return self.nome

    # Metadados do modelo.
    class Meta:
        # Define o nome no plural que será exibido no painel de administração.
        verbose_name_plural = "Cidades"

# Modelo para representar as categorias das atrações
class Categoria(models.Model):
    # Campo para o nome da categoria, com um máximo de 100 caracteres e deve ser único.
    nome = models.CharField(max_length=100, unique=True)
    # Campo para a classe do ícone (ex: do Font Awesome).
    icone = models.CharField(max_length=50, help_text="Ex: 'fas fa-tree'. Use classes do Font Awesome.")

    # Define a representação em string do objeto, que será o nome da categoria.
    def __str__(self):
        return self.nome

# Modelo principal para as atrações turísticas
class Atracao(models.Model):
    # Campos de texto para informações básicas da atração.
    nome = models.CharField(max_length=200)
    descricao = models.TextField(help_text="Descrição detalhada da atração.")
    horario_funcionamento = models.CharField(max_length=200, blank=True, null=True)
    informacoes_entrada = models.CharField(max_length=200, blank=True, null=True, help_text="Ex: 'Gratuita', 'Consultar valores'.")
    
    # Campo de imagem. 'upload_to' define um diretório temporário inicial.
    # O caminho final será ajustado no método save().
    imagem = models.ImageField(upload_to='atracoes/temp/', help_text="Imagem principal da atração.")
    
    # Campos para coordenadas geográficas, permitindo valores nulos.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            super().save(*args, **kwargs)
            # Remove force_insert before the possible second save
            kwargs.pop('force_insert', None)

        # 2. Verifica se uma imagem foi enviada e se ela ainda está no diretório temporário.
        image_moved = False
        if self.imagem and self.imagem.name.startswith('atracoes/temp/'):
            old_name = self.imagem.name
            filename = os.path.basename(old_name)
            new_path = atracao_image_path(self, filename)
            
            try:
                renamed_file = default_storage.save(new_path, self.imagem.file)
                self.imagem.name = renamed_file
                if default_storage.exists(old_name):
                    default_storage.delete(old_name)
                image_moved = True
            except Exception as e:
                print(f"Erro ao mover o arquivo de imagem: {e}")
                pass 
        
        # 3. Salva a instância novamente apenas se for uma atualização (não novo) ou se a imagem mudou
        if not is_new or image_moved:
            super().save(*args, **kwargs)

    # --- Relacionamentos com outros modelos (Chaves Estrangeiras) ---
    # Relaciona a Atração a uma Cidade. `on_delete=models.PROTECT` impede que uma cidade com atrações seja deletada.
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, related_name='atracoes')
    # Relaciona a Atração a uma Categoria.
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='atracoes')

    def __str__(self):
        return self.nome

# --- Modelo de Usuário ---
class Usuario(models.Model):
    # Esta linha importa o modelo de usuário padrão do Django, mas não o utiliza dentro desta classe.
    from django.contrib.auth.models import User