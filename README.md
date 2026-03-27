# 🗺️ TurMaps | Guia Interativo da Região de Carajás

O **TurMaps** é uma plataforma web desenvolvida em Python/Django focada na valorização e exploração do turismo na região de Carajás (Parauapebas, Canaã dos Carajás e Curionópolis). 

O sistema não é apenas um catálogo digital, mas uma ferramenta de **Tech-Growth** projetada para entregar valor imediato a moradores e visitantes (como profissionais da mineração), centralizando a descoberta de parques, balneários e mirantes através de uma interface interativa e responsiva.

## ⚙️ Arquitetura e Funcionalidades

* **Mapa Interativo Inteligente:** Integração com a biblioteca Leaflet.js e MarkerCluster. Os marcadores de localização são renderizados dinamicamente e agrupados automaticamente para otimizar o desempenho visual e não poluir o front-end.
* **Sistema de Filtragem Dinâmica:** Algoritmo de busca cruzada (por Cidade e Categoria) que atualiza o mapa e os resultados em tempo real, melhorando a retenção do usuário (UX).
* **Painel Administrativo Customizado (CRUD):** Desenvolvimento de uma área restrita direto no front-end. Administradores podem gerenciar (Adicionar, Editar, Excluir) atrações de forma intuitiva, substituindo o painel padrão do Django por uma experiência focada no usuário final.
* **Gestão de Identidade e Acesso (IAM):** Sistema completo de autenticação e autorização. Rotas protegidas garantem que funções de gerenciamento sejam acessíveis exclusivamente pela equipe técnica/admin.

## 🛠️ Stack Tecnológica

* **Back-end:** Python 3, Django
* **Front-end:** HTML5, CSS3, JavaScript (Vanilla)
* **Geolocalização & Mapas:** Leaflet.js, Leaflet.markercluster
* **Banco de Dados:** SQLite (com modelagem relacional estruturada para futura migração para PostgreSQL)

## 🛡️ Visão de Produto e Próximos Passos (Roadmap)

Este projeto foi desenhado com escalabilidade em mente. As próximas sprints incluem:
1. **Migração de Banco de Dados:** Transição para PostgreSQL para suportar maior volume de consultas simultâneas.
2. **Sistema de Avaliações (Rating):** Implementação de reviews de usuários logados para gerar prova social.
3. **Geolocalização Ativa:** Integração com a API de GPS do navegador para centralizar o mapa em "Atrações perto de mim".
