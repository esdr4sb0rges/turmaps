import os
import django

# Define as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_django.settings')
django.setup()

from crud_app.models import Cidade, Categoria, Atracao

def run_seed():
    print("Iniciando a população do banco de dados (SEED)...")

    # 1. Cidades
    print("Criando cidades...")
    cidade_parauapebas, _ = Cidade.objects.get_or_create(nome="Parauapebas")
    cidade_canaa, _ = Cidade.objects.get_or_create(nome="Canaã dos Carajás")

    # 2. Categorias
    print("Criando categorias...")
    cat_parques, _ = Categoria.objects.get_or_create(
        nome="Complexos e Parques", 
        defaults={"icone": "fas fa-tree"}
    )
    cat_natureza, _ = Categoria.objects.get_or_create(
        nome="Natureza e Aventura", 
        defaults={"icone": "fas fa-leaf"}
    )
    cat_cultura, _ = Categoria.objects.get_or_create(
        nome="Cultura e Histórico", 
        defaults={"icone": "fas fa-landmark"}
    )
    cat_lazer, _ = Categoria.objects.get_or_create(
        nome="Lazer e Compras", 
        defaults={"icone": "fas fa-shopping-bag"}
    )

    # 3. Atrações (Genérico coords para Parauapebas -1.45, -48.49)
    # Lista fornecida
    atracoes_parauapebas = [
        {"nome": "Complexo Turístico de Parauapebas", "cat": cat_parques},
        {"nome": "Parque dos Ipês", "cat": cat_parques},
        {"nome": "Parque Zoobotânico de Carajás", "cat": cat_parques},
        {"nome": "Clube City Park", "cat": cat_lazer},
        {"nome": "Águas Termais Garimpo das Pedras", "cat": cat_natureza},
        {"nome": "Rapel em Cachoeira", "cat": cat_natureza},
        {"nome": "Lagoas Serra Sul", "cat": cat_natureza},
        {"nome": "Birdwatch", "cat": cat_natureza},
        {"nome": "Serra Pelada", "cat": cat_cultura},
        {"nome": "Mirante Vale do Rio Azul", "cat": cat_natureza},
        {"nome": "Mirante Flor de Carajás", "cat": cat_natureza},
        {"nome": "Rio Jordão", "cat": cat_natureza},
        {"nome": "Estância Águas de Maria", "cat": cat_lazer},
        {"nome": "Balneário do Joca", "cat": cat_lazer},
        {"nome": "Balneário Prainha", "cat": cat_lazer},
        {"nome": "Avião DC-3", "cat": cat_cultura},
        {"nome": "Praça da Bíblia", "cat": cat_cultura},
        {"nome": "Prefeitura de Parauapebas", "cat": cat_cultura},
        {"nome": "Shopping Partage", "cat": cat_lazer},
        {"nome": "Shopping Karajas", "cat": cat_lazer},
        {"nome": "Centro Cultural de Parauapebas", "cat": cat_cultura},
        {"nome": "Estação Ferroviária", "cat": cat_cultura},
        {"nome": "Centro Mulheres de Barro", "cat": cat_cultura},
        {"nome": "Ginásio Poliesportivo", "cat": cat_lazer},
        {"nome": "Oca Parauapebas", "cat": cat_cultura},
        {"nome": "Praça dos Metais", "cat": cat_cultura},
    ]

    atracoes_canaa = [
        {"nome": "Veredas", "cat": cat_parques},
        {"nome": "Lago da Prefeitura", "cat": cat_parques},
        {"nome": "Lago da Buriti", "cat": cat_parques},
        {"nome": "Usina da Paz", "cat": cat_lazer},
        {"nome": "Complexo Poliesportivo", "cat": cat_lazer},
        {"nome": "Aqua Park", "cat": cat_lazer},
        {"nome": "Letreiro da Cidade", "cat": cat_cultura},
        {"nome": "Praça da Bíblia", "cat": cat_cultura},
    ]

    print("Criando atrações de Parauapebas...")
    for index, item in enumerate(atracoes_parauapebas):
        # Deslocamento artificial para as coordenadas não ficarem no mesmo ponto exato
        # Base: -1.45, -48.49
        lat = -1.45 + (index * 0.001)
        lon = -48.49 + (index * 0.001)
        Atracao.objects.get_or_create(
            nome=item["nome"],
            cidade=cidade_parauapebas,
            defaults={
                "descricao": f"Descrição padrão para {item['nome']}.",
                "categoria": item["cat"],
                "latitude": lat,
                "longitude": lon,
                "horario_funcionamento": "08:00 às 18:00",
                "informacoes_entrada": "Gratuita",
                "imagem": ""
            }
        )

    print("Criando atrações de Canaã dos Carajás...")
    for index, item in enumerate(atracoes_canaa):
        lat = -1.46 + (index * 0.001)  # Coordenada hipotética
        lon = -48.50 + (index * 0.001)
        Atracao.objects.get_or_create(
            nome=item["nome"],
            cidade=cidade_canaa,
            defaults={
                "descricao": f"Descrição padrão para {item['nome']}.",
                "categoria": item["cat"],
                "latitude": lat,
                "longitude": lon,
                "horario_funcionamento": "08:00 às 18:00",
                "informacoes_entrada": "Gratuita",
                "imagem": ""
            }
        )

    print("Seed concluído com sucesso!")

if __name__ == '__main__':
    run_seed()
