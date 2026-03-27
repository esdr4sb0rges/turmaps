# Importa a classe base de configuração de aplicativos do Django.
from django.apps import AppConfig

# Define a classe de configuração para o aplicativo 'crud_app'.
# O Django usa esta classe para saber como o aplicativo deve ser carregado e configurado.
class CrudAppConfig(AppConfig):
    # Define o tipo de campo padrão para chaves primárias automáticas (como 'id').
    # 'BigAutoField' é um inteiro de 64 bits, o que é bom para escalabilidade.
    default_auto_field = 'django.db.models.BigAutoField'
    # Especifica o nome do aplicativo ao qual esta configuração se aplica.
    name = 'crud_app'
