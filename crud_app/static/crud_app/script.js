// ===============================================
// 1. LÓGICA GERAL (Funções Comuns)
// ===============================================
// Adiciona um 'escutador' de eventos que espera o DOM (a estrutura da página) ser completamente carregado antes de executar qualquer script.
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa a função do menu mobile (hambúrguer) em todas as páginas.
    setupMobileMenu();

    // --- Lógica Específica da Página ---
    // Verifica a existência de elementos específicos de cada página para chamar a função de setup correspondente.
    // Isso evita erros no console ao tentar manipular elementos que não existem na página atual.
    if (document.getElementById('cadastroForm')) {
        setupCadastroForm();
    }
    if (document.getElementById('contactForm')) {
        setupContatoForm();
    }
    if (document.getElementById('attractions-container')) {
        setupIndexAttractions();
    }
    if (document.getElementById('attractions-grid')) {
        setupAtracoesFilters();
    }
    // A lógica do mapa é inicializada via initInteractiveMap() no template mapa.html
});

/**
 * Configura a funcionalidade do menu de navegação para dispositivos móveis.
 */
function setupMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    // Garante que os elementos do menu existem antes de adicionar os eventos.
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            // Alterna a classe 'active' para mostrar ou esconder o menu.
            navLinks.classList.toggle('active');
            
            // Altera o ícone do botão entre "hambúrguer" e "X".
            const icon = menuToggle.querySelector('i');
            icon.className = navLinks.classList.contains('active') ? 'fas fa-times' : 'fas fa-bars';
        });

        // Adiciona um evento a cada link do menu para que ele se feche após um clique.
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
                menuToggle.querySelector('i').className = 'fas fa-bars';
            });
        });
    }
}

// ===============================================
// 2. LÓGICA INDEX.HTML
// ===============================================

/**
 * Configura os filtros de cidade e a barra de busca da página inicial.
 */
function setupIndexAttractions() {
    const cityTabs = document.querySelectorAll('.city-tab');
    const attractionCards = document.querySelectorAll('.attraction-card');
    const searchInput = document.querySelector('.search-bar input');
    const searchButton = document.querySelector('.search-bar button');
    
    // Funções de Filtragem por Tabs
    cityTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            cityTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            const selectedCity = this.getAttribute('data-city');
            
            // Itera sobre todos os cards de atração.
            attractionCards.forEach(card => {
                const cardCity = card.getAttribute('data-city');
                // Mostra o card se a cidade selecionada for 'todos' ou se a cidade do card corresponder à selecionada.
                if (selectedCity === 'todos' || cardCity === selectedCity) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    /**
     * Executa a lógica de busca, filtrando os cards com base no termo digitado.
     */
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        // Itera sobre os cards, verificando se o termo de busca está presente no título, descrição ou categoria.
        attractionCards.forEach(card => {
            const cardTitle = card.querySelector('h3').textContent.toLowerCase();
            const cardDescription = card.querySelector('.card-description').textContent.toLowerCase();
            const cardCategory = card.querySelector('.card-category').textContent.toLowerCase();
            
            // Se o campo de busca estiver vazio ou se houver correspondência, o card é exibido.
            if (searchTerm === '' || 
                cardTitle.includes(searchTerm) || 
                cardDescription.includes(searchTerm) || 
                cardCategory.includes(searchTerm)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });

        // Se uma busca for feita, reseta a seleção das abas de cidade para "Todos".
        if (searchTerm !== '') {
            cityTabs.forEach(t => t.classList.remove('active'));
            const todosTab = document.querySelector('.city-tab[data-city="todos"]');
            if (todosTab) todosTab.classList.add('active');
        }
    }

    // Adiciona eventos de clique ao botão de busca e de "Enter" no campo de input.
    if (searchButton) {
        searchButton.addEventListener('click', function(e) {
            e.preventDefault();
            performSearch();
        });
    }

    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }
    
    // Funções de Mapa (Simulação para o botão da seção de mapa na index)
    window.showMapDemo = function() {
        const placeholder = document.getElementById('map-placeholder');
        if (placeholder) {
            placeholder.innerHTML = `<div class="map-placeholder-content"><i class="fas fa-spinner fa-spin"></i><h3>Carregando Demo...</h3></div>`;
            setTimeout(() => { location.reload(); }, 3000);
        }
    }
}

// ===============================================
// 3. LÓGICA ATRACOES.HTML
// ===============================================

/**
 * Configura os filtros de categoria e cidade na página de listagem de atrações.
 */
function setupAtracoesFilters() {
    const categoryButtons = document.querySelectorAll('.filter-btn');
    const citySelect = document.getElementById('city-filter-select');
    const attractionCards = document.querySelectorAll('.attraction-card');

    // Variáveis para armazenar o estado atual dos filtros.
    let currentCategory = 'all';
    let currentCity = 'all';

    /**
     * Filtra os cards de atração com base nos valores de `currentCategory` e `currentCity`.
     */
    function filterAttractions() {
        attractionCards.forEach(card => {
            const cardCategory = card.dataset.category;
            const cardCity = card.dataset.city;

            // Verifica se o card corresponde aos filtros selecionados.
            const categoryMatch = (currentCategory === 'all' || currentCategory === cardCategory);
            const cityMatch = (currentCity === 'all' || currentCity === cardCity);

            if (categoryMatch && cityMatch) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // Adiciona eventos de clique aos botões de categoria.
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            currentCategory = button.dataset.filter;
            filterAttractions();
        });
    });

    // Adiciona evento de mudança ao seletor de cidade.
    if (citySelect) {
        citySelect.addEventListener('change', () => {
            currentCity = citySelect.value;
            filterAttractions();
        });
    }
}


// ===============================================
// 4. LÓGICA CONTATO.HTML
// ===============================================

/**
 * Configura o formulário de contato, incluindo validação e simulação de envio.
 */
function setupContatoForm() {
    const contactForm = document.getElementById('contactForm');
    const successMessage = document.getElementById('successMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // Previne o envio padrão do formulário para simular uma resposta de sucesso no front-end.
            e.preventDefault(); // Mantido para simular o comportamento de sucesso do front-end
            
            const nome = document.getElementById('nome').value.trim();
            const email = document.getElementById('email').value.trim();
            const assunto = document.getElementById('assunto').value.trim();
            const mensagem = document.getElementById('mensagem').value.trim();

            // Validação simples de campos vazios e formato de e-mail.
            if (nome === '' || email === '' || assunto === '' || mensagem === '') {
                alert('Por favor, preencha todos os campos obrigatórios.');
                return;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Por favor, insira um e-mail válido.');
                return;
            }

            // Simulação de sucesso: exibe a mensagem de sucesso e limpa o formulário.
            // Em um cenário real com AJAX, isso seria chamado na resposta de sucesso da requisição.
            console.log('Formulário enviado:', { nome, email, assunto, mensagem });
            
            successMessage.classList.add('show');
            contactForm.reset();
            
            // Esconde a mensagem de sucesso após 5 segundos.
            setTimeout(function() {
                successMessage.classList.remove('show');
            }, 5000);
        });
    }
}

// ===============================================
// 5. LÓGICA CADASTRO.HTML
// ===============================================

/**
 * Configura o formulário de cadastro, incluindo máscara de CPF, indicador de força de senha e validações.
 */
function setupCadastroForm() {
    const cpfInput = document.getElementById('cpf');
    const senhaInput = document.getElementById('senha');
    const confirmarSenha = document.getElementById('confirmarSenha');
    const cadastroForm = document.getElementById('cadastroForm');
    
    const passwordStrength = document.getElementById('passwordStrength');
    const strengthBarFill = document.getElementById('strengthBarFill');
    const strengthText = document.getElementById('strengthText');
    const successModal = document.getElementById('successModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    
    /**
     * Valida um número de CPF.
     * @param {string} cpf - O CPF a ser validado.
     */
    function validarCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
        let soma = 0, resto;
        for (let i = 1; i <= 9; i++) soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
        resto = (soma * 10) % 11;
        if (resto === 10 || resto === 11) resto = 0;
        if (resto !== parseInt(cpf.substring(9, 10))) return false;
        soma = 0;
        for (let i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
        resto = (soma * 10) % 11;
        if (resto === 10 || resto === 11) resto = 0;
        if (resto !== parseInt(cpf.substring(10, 11))) return false;
        return true;
    }

    // Aplica a máscara de formatação (###.###.###-##) ao campo de CPF enquanto o usuário digita.
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                e.target.value = value;
            }
        });
    }

    // Analisa a senha digitada e exibe um indicador de força (fraca, média, forte).
    if (senhaInput) {
        senhaInput.addEventListener('input', function() {
            const senha = this.value;
            passwordStrength.classList.add('show');
            
            // Lógica de pontuação de força da senha.
            let strength = 0;
            if (senha.length >= 6) strength++;
            if (senha.length >= 10) strength++;
            if (/[a-z]/.test(senha) && /[A-Z]/.test(senha)) strength++;
            if (/\d/.test(senha)) strength++;
            if (/[^a-zA-Z\d]/.test(senha)) strength++;
            
            // Atualiza a cor da barra e o texto com base na pontuação.
            strengthBarFill.className = 'strength-bar-fill';
            
            if (strength <= 2) {
                strengthBarFill.classList.add('weak');
                strengthText.textContent = 'Senha fraca';
                strengthText.style.color = '#dc3545';
            } else if (strength <= 4) {
                strengthBarFill.classList.add('medium');
                strengthText.textContent = 'Senha média';
                strengthText.style.color = '#ffc107';
            } else {
                strengthBarFill.classList.add('strong');
                strengthText.textContent = 'Senha forte';
                strengthText.style.color = '#28a745';
            }
        });
    }

    // Adiciona validações no lado do cliente antes de permitir o envio do formulário.
    if (cadastroForm) {
        cadastroForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            const senha = senhaInput.value;
            const cpf = cpfInput.value;
            const termos = document.getElementById('termos').checked;

            if (senha !== confirmarSenha.value) { /* set error */ isValid = false; }
            if (!validarCPF(cpf)) { /* set error */ isValid = false; }
            if (!termos) { alert('Você deve aceitar os Termos de Uso.'); isValid = false; }

            // Se a validação falhar, o envio do formulário para o backend é prevenido.
            if (!isValid) {
                e.preventDefault(); // Previne o POST para o Django se a validação falhar
            }
            
            // Nota: Se a view do Django retornar sucesso, ela fará o redirect. 
            // O modal só é útil se a submissão for via AJAX e não POST padrão.
            // Para manter o fluxo POST, removemos a lógica de exibição de modal aqui.
        });
    }
}


// ===============================================
// 6. LÓGICA MAPA.HTML
// ===============================================

// Variáveis globais para o mapa (preenchidas na inicialização)
let allAttractionsData = []; // Armazena o JSON completo do backend
let filteredAttractions = []; // Armazena a lista filtrada
let currentMapUrl = "about:blank"; 
let map = null;
let markersLayer = null;

/**
 * 🎯 Função de inicialização principal. Chamada do bloco JS de mapa.html.
 * Recebe os dados das atrações (em formato JSON) da view do Django e inicia a interface do mapa.
 */
window.initInteractiveMap = function(data) {
    allAttractionsData = data;
    filteredAttractions = [...data];
    
    // Inicializa o mapa do Leaflet apenas se não existir
    if (!map) {
        map = L.map('map-iframe').setView([-1.45, -48.49], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        markersLayer = L.layerGroup().addTo(map);
    }
    
    setupMapUIAndEvents();
    renderAttractionsList(allAttractionsData); // Renderiza a lista inicial
    updateStats();
    
    // Renderiza os pins no map
    renderMapMarkers(allAttractionsData);

    // Foca na região com mais itens automaticamente
    if (filteredAttractions.length > 0) {
        window.focusOnComplexo();
    }
};

/**
 * Renderiza os pinos (markers) no mapa Leaflet baseado nos dados filtrados.
 */
function renderMapMarkers(dataArray) {
    if (!markersLayer) return;
    markersLayer.clearLayers();
    
    const bounds = [];
    
    dataArray.forEach(atracao => {
        if (atracao.latitude && atracao.longitude && atracao.latitude != 0 && atracao.longitude != 0) {
            const latlng = [atracao.latitude, atracao.longitude];
            const marker = L.marker(latlng)
                .bindPopup(`<b>${atracao.nome}</b><br>${atracao.categoria}<br><br><button onclick="focusOnAttractionById(${atracao.id})" class="map-btn" style="font-size: 0.8em; padding: 5px;">Ver Detalhes</button>`);
            markersLayer.addLayer(marker);
            bounds.push(latlng);
        }
    });

    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [30, 30] });
    }
}

window.focusOnAttractionById = function(id) {
    const attraction = allAttractionsData.find(a => a.id === id);
    if (attraction) {
        focusOnAttraction(attraction);
    }
};

/**
 * Renderiza a lista de atrações na barra lateral.
 * @param {Array} attractionsArray - O array de atrações a ser renderizado.
 */
function renderAttractionsList(attractionsArray) {
    const listContainer = document.getElementById('attractions-list');
    if (!listContainer) return;
    
    listContainer.innerHTML = ''; 

    // Se não houver atrações, exibe uma mensagem.
    if (attractionsArray.length === 0) {
        listContainer.innerHTML = '<p style="text-align: center; color: var(--cinza-medio); padding-top: 10px;">Nenhuma atração cadastrada ou encontrada com os filtros.</p>';
        return;
    }

    // Cria um card HTML para cada atração e o insere no container.
    attractionsArray.forEach(atracao => {
        // Usa as classes definidas no style.css para a listagem lateral do mapa.
        const cardHTML = `
            <div class="attraction-item" 
                 data-id="${atracao.id}" 
                 data-category="${atracao.categoria_slug}" 
                 data-city="${atracao.cidade_slug}"
                 onclick="selectAttraction(this)">
                
                <div class="attraction-header">
                    <div class="attraction-icon">
                        <i class="${atracao.icone}"></i>
                    </div>
                    <div class="attraction-name">${atracao.nome}</div>
                    <div class="attraction-category">${atracao.categoria}</div>
                </div>
                <div class="attraction-city">${atracao.cidade}</div>
            </div>
        `;
        listContainer.insertAdjacentHTML('beforeend', cardHTML);
    });
}

/**
 * Configura os eventos de clique e mudança para os filtros da barra lateral.
 */
function setupMapUIAndEvents() {
    const cityFilter = document.getElementById('city-filter');
    const categoryButtons = document.querySelectorAll('#category-filter-buttons .filter-btn');

    // Eventos de Filtragem
    if (cityFilter) {
        cityFilter.addEventListener('change', applyFilters);
    }
    categoryButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            categoryButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            applyFilters();
        });
    });
}

/**
 * Coleta os valores dos filtros, filtra o array de dados e atualiza a interface.
 */
function applyFilters() {
    const cityFilterElement = document.getElementById('city-filter');
    const categoryButtonElement = document.querySelector('#category-filter-buttons .filter-btn.active');
    
    // Verifica se os elementos foram encontrados
    if (!cityFilterElement || !categoryButtonElement) {
        console.error("Elementos de filtro não encontrados para aplicar a lógica.");
        return;
    }

    const cityValue = cityFilterElement.value;
    const categoryFilter = categoryButtonElement.getAttribute('data-filter');
    
    // 1. Filtra o array completo de atrações (allAttractionsData)
    filteredAttractions = allAttractionsData.filter(attraction => {
        // Se a latitude/longitude não estiverem presentes, a atração é incluída, mas não aparecerá no mapa.
        const cityMatch = cityValue === 'all' || attraction.cidade_slug === cityValue;
        const categoryMatch = categoryFilter === 'all' || attraction.categoria_slug === categoryFilter;
        return cityMatch && categoryMatch;
    });
    
    // 2. Renderiza a nova lista e atualiza estatísticas
    renderAttractionsList(filteredAttractions);
    renderMapMarkers(filteredAttractions);
    updateStats();
    
    // 3. Foca o mapa nos resultados filtrados
    if (filteredAttractions.length > 0) {
        const infoPanel = document.getElementById('info-panel');
        if (infoPanel) infoPanel.classList.add('hidden');
    }
}

/**
 * Centraliza o mapa em uma atração específica e atualiza o painel de informações.
 * @param {Object} atracao - O objeto da atração a ser focado.
 */
function focusOnAttraction(atracao) {
    const lat = atracao.latitude;
    const lng = atracao.longitude;
    const infoPanel = document.getElementById('info-panel');
    
    // Verifica se a atração possui coordenadas válidas.
    if (lat && lng && lat != 0 && lng != 0) {
        // Centraliza o mapa do Leaflet
        if (map) {
            map.setView([lat, lng], 16);
        }
        
        // Atualiza o painel de informações com os detalhes da atração.
        if (infoPanel) {
            infoPanel.innerHTML = `
                <div class="info-panel-content">
                    <div class="info-header">
                        <div class="info-icon"><i class="${atracao.icone}"></i></div>
                        <h3 class="info-title">${atracao.nome}</h3>
                    </div>
                    <div class="info-body">
                        <p class="info-description">${atracao.descricao}</p>
                        <div class="info-details">
                            <div class="info-item">
                                <i class="fas fa-map-marker-alt"></i>
                                <span>${atracao.cidade}</span>
                            </div>
                            <div class="info-item">
                                <i class="fas fa-tag"></i>
                                <span>${atracao.categoria}</span>
                            </div>
                            <div class="info-item">
                                <i class="fas fa-clock"></i>
                                <span>${atracao.horario}</span>
                            </div>
                            <div class="info-item">
                                <i class="fas fa-ticket-alt"></i>
                                <span>${atracao.entrada}</span>
                            </div>
                        </div>
                    </div>
                    ${atracao.imagem_url ? `<img src="${atracao.imagem_url}" alt="${atracao.nome}" class="info-image" style="width:100%; object-fit: cover; border-radius: 8px; margin-top: 15px; max-height:200px;">` : ''}
                </div>
            `;
            infoPanel.classList.remove('hidden');
        }
        
        // Armazena a URL para o botão "Abrir no Google Maps".
        currentMapUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;
        
    } else {
        if (infoPanel) {
            infoPanel.innerHTML = `
                <div class="info-panel-content">
                    <p style="text-align: center; color: var(--cinza-medio); padding: 20px;">📍 Coordenadas não disponíveis para esta atração.</p>
                </div>
            `;
            infoPanel.classList.remove('hidden');
        }
        currentMapUrl = 'about:blank';
    }
}

/**
 * Atualiza os contadores de estatísticas (total de atrações e visíveis) na barra lateral.
 */
function updateStats() {
    const totalAttractions = document.getElementById('total-attractions');
    const visibleCount = document.getElementById('visible-attractions');

    if (totalAttractions) totalAttractions.textContent = allAttractionsData.length;
    if (visibleCount) visibleCount.textContent = filteredAttractions.length;
    if (document.getElementById('visible-count')) document.getElementById('visible-count').textContent = `(${filteredAttractions.length})`;
}


// --- Funções Globais Chamadas pelo HTML ---

// Limpa todos os filtros aplicados e re-renderiza a lista.
window.clearAllFilters = function() {
    document.getElementById('city-filter').value = 'all';
    document.querySelectorAll('#category-filter-buttons .filter-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector('.filter-btn[data-filter="all"]').classList.add('active');
    applyFilters();
};

// Foca o mapa na localização central ou na primeira atração da lista.
window.focusOnComplexo = function() { 
    if (filteredAttractions.length > 0) {
        const bounds = filteredAttractions
            .filter(a => a.latitude && a.longitude && a.latitude != 0 && a.longitude != 0)
            .map(a => [a.latitude, a.longitude]);
            
        if (bounds.length > 0 && map) {
            map.fitBounds(bounds, { padding: [30, 30] });
        }
    } else {
        alert("Nenhuma atração cadastrada para focar.");
    }
};

// Alterna a visibilidade do painel de informações.
window.toggleInfoPanel = function() {
    const panel = document.getElementById('info-panel');
    const icon = document.getElementById('toggle-icon');
    if (panel && icon) {
        panel.classList.toggle('hidden');
        icon.className = panel.classList.contains('hidden') ? 'fas fa-eye' : 'fas fa-info';
    }
};

// Exibe um alerta com as instruções de uso do mapa.
window.showMapInstructions = function() { 
     alert(`🗺️ INSTRUÇÕES DO MAPA INTERATIVO\\n\\n` +
          `1. Filtros: Use os menus e botões laterais para restringir a lista de atrações.\\n` +
          `2. Seleção: Clique em qualquer item da lista para centralizar o mapa na localização e exibir o painel de informações.\\n` +
          `3. Controles:\\n` +
          `   - Focar no Ponto Central: Volta o mapa para a localização inicial.\\n` +
          `   - Abrir no Google Maps: Abre a atração selecionada em uma nova aba para navegação.`);
};

// Abre a localização da atração selecionada em uma nova aba no Google Maps.
window.openInGoogleMaps = function() {
    if (currentMapUrl && currentMapUrl !== 'about:blank') {
        window.open(currentMapUrl, '_blank');
    } else {
        alert('Nenhuma atração selecionada ou coordenadas não disponíveis.');
    }
};

/**
 * Chamada quando um item da lista de atrações é clicado.
 * @param {HTMLElement} element - O elemento do card da atração que foi clicado.
 */
window.selectAttraction = function(element) {
    // Remove a classe 'active' ou 'selected' de todos os outros itens.
    document.querySelectorAll('.attraction-item').forEach(item => {
        item.classList.remove('active'); // Usando 'active' para consistência com outros filtros
    });
    
    // Adiciona a classe 'active' ao item clicado para destaque visual.
    element.classList.add('active');
    
    // Busca a atração correspondente no array de dados
    const attractionId = parseInt(element.dataset.id);
    const selectedAttraction = allAttractionsData.find(a => a.id === attractionId);
    
    if (selectedAttraction) {
        focusOnAttraction(selectedAttraction);
    }
};