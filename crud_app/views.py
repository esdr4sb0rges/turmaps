from django.shortcuts import render, redirect, get_object_or_404
# Importa o modelo de usuário padrão do Django e funções de autenticação
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Importa os modelos da aplicação
from .models import Atracao, Categoria, Cidade
#Ativa o requerimento de login para certas views


# ----------------------------------------------------------------------
# Views para as páginas do site TurMaps
# ----------------------------------------------------------------------

def index(request):
    """
    Carrega as atrações, categorias e cidades para exibir na página inicial.
    """
    # Busca as 6 primeiras atrações, otimizando a consulta com `select_related` para buscar
    # os dados de Cidade e Categoria em uma única query.
    atracoes_list = Atracao.objects.select_related('cidade', 'categoria').all()[:6]
    categorias = Categoria.objects.all()
    cidades = Cidade.objects.all()
    
    # Monta o dicionário de contexto para ser enviado ao template.
    context = {
        'atracoes': atracoes_list,
        'categorias': categorias,
        'cidades': cidades,
    }
    return render(request, 'crud_app/index.html', context)

@staff_member_required
def atracoes_admin_index(request):
    """
    Exibe a lista completa de atrações para gerenciamento.
    """
    # Busca todas as atrações, ordenando por nome, e otimiza a consulta com `select_related`.
    atracoes_list = Atracao.objects.select_related('cidade', 'categoria').all().order_by('nome')
    
    # Monta o contexto com a lista de atrações.
    context = {
        'atracoes': atracoes_list,
    }
    # Renderiza o template específico para a administração de atrações.
    return render(request, 'crud_app/atracoes_admin_index.html', context)

@staff_member_required # Garante que só admins acessem esta view
def atracoes_create(request):
    # Garante que as listas de objetos sejam carregadas, mesmo em caso de erro de POST
    cidades = Cidade.objects.all().order_by('nome')
    categorias = Categoria.objects.all().order_by('nome')

    error_message = None

    # Verifica se a requisição é do tipo POST (envio de formulário).
    if request.method == 'POST':
        # --- 1. Lógica da CIDADE ---
        cidade_id = request.POST.get('cidade_id_existente')
        nova_cidade_nome = request.POST.get('nova_cidade_nome', '').strip()
        cidade = None
        
        if cidade_id:
            # Se o usuário selecionou uma cidade existente, busca ela no banco.
            cidade = get_object_or_404(Cidade, pk=cidade_id)
        elif nova_cidade_nome:
            # Se o usuário digitou um nome para uma nova cidade, cria ou obtém a existente.
            try:
                cidade, created = Cidade.objects.get_or_create(nome=nova_cidade_nome)
            except Exception as e:
                error_message = f'Erro ao criar Cidade: {e}'

        # --- 2. Lógica da CATEGORIA ---
        categoria_id = request.POST.get('categoria_id_existente')
        nova_categoria_nome = request.POST.get('nova_categoria_nome', '').strip()
        nova_categoria_icone = request.POST.get('nova_categoria_icone', '').strip()
        categoria = None
        
        if categoria_id:
            # Se o usuário selecionou uma categoria existente, busca ela no banco.
            categoria = get_object_or_404(Categoria, pk=categoria_id)
        elif nova_categoria_nome and nova_categoria_icone:
            # Se o usuário preencheu os dados de uma nova categoria, cria ou obtém a existente.
            try:
                categoria, created = Categoria.objects.get_or_create(
                    nome=nova_categoria_nome,
                    defaults={'icone': nova_categoria_icone}
                )
            except Exception as e:
                error_message = f'Erro ao criar Categoria: {e}'
        
        # --- 3. Lógica da ATRAÇÃO ---
        # Apenas prossegue se uma cidade e uma categoria foram definidas e não houve erros.
        if cidade and categoria and not error_message:
            try:
                # Cria a nova instância de Atracao com os dados do formulário.
                Atracao.objects.create(
                    nome=request.POST.get('nome'),
                    descricao=request.POST.get('descricao'),
                    horario_funcionamento=request.POST.get('horario_funcionamento'),
                    informacoes_entrada=request.POST.get('informacoes_entrada'),
                    imagem=request.FILES.get('imagem'), 
                    latitude=request.POST.get('latitude'),
                    longitude=request.POST.get('longitude'),
                    cidade=cidade,
                    categoria=categoria,
                )
                # Redireciona para a página de lista de atrações após o sucesso.
                return redirect('atracoes') 
            except Exception as e:
                error_message = f'Erro ao salvar atração: {e}'
        elif not cidade or not categoria:
             error_message = 'Por favor, selecione uma Cidade e uma Categoria existentes, ou preencha os campos para criar novas.'

    # --- 4. Contexto para GET ou POST com erro ---
    # Contexto para a requisição GET ou em caso de erro no POST
    context = {
        'cidades': Cidade.objects.all().order_by('nome'),
        'categorias': Categoria.objects.all().order_by('nome'),
        'error': error_message
    }
    return render(request, 'crud_app/atracoes_create.html', context)

    # Contexto para a requisição GET (exibir o formulário vazio).
    context = {
        'cidades': cidades,
        'categorias': categorias
    }
    return render(request, 'crud_app/atracoes_create.html', context)

@staff_member_required
def atracoes_edit(request, id):
    # Busca a atração específica pelo ID ou retorna um erro 404 se não encontrar.
    atracao = get_object_or_404(Atracao, pk=id)
    # Busca todas as cidades e categorias para preencher os seletores do formulário.
    cidades = Cidade.objects.all().order_by('nome')
    categorias = Categoria.objects.all().order_by('nome')
    error_message = None

    # Se o formulário foi submetido (método POST).
    if request.method == 'POST':
        # Busca a cidade e categoria selecionadas no formulário.
        cidade = get_object_or_404(Cidade, pk=request.POST.get('cidade'))
        categoria = get_object_or_404(Categoria, pk=request.POST.get('categoria'))
        
        try:
            # Atualiza os campos do objeto 'atracao' com os dados vindos do formulário.
            atracao.nome = request.POST.get('nome')
            atracao.descricao = request.POST.get('descricao')
            atracao.horario_funcionamento = request.POST.get('horario_funcionamento')
            atracao.informacoes_entrada = request.POST.get('informacoes_entrada')
            atracao.latitude = request.POST.get('latitude')
            atracao.longitude = request.POST.get('longitude')
            atracao.cidade = cidade
            atracao.categoria = categoria
            
            # Verifica se um novo arquivo de imagem foi enviado.
            if request.FILES.get('imagem'):
                atracao.imagem = request.FILES.get('imagem')
            
            # Salva as alterações no banco de dados.
            atracao.save()
            # Redireciona para a página de administração de atrações.
            return redirect('atracoes_admin_index')
            
        except Exception as e:
            error_message = f'Erro ao atualizar atração: {e}'

    # Monta o contexto para ser enviado ao template (seja em GET ou em caso de erro no POST).
    context = {
        'atracao': atracao,
        'cidades': cidades,
        'categorias': categorias,
        'error': error_message
    }
    return render(request, 'crud_app/atracoes_edit.html', context)

@staff_member_required
def atracoes_delete(request, id):
    # Busca a atração a ser deletada.
    atracao = get_object_or_404(Atracao, pk=id)

    # Se o usuário confirmou a exclusão (requisição POST).
    if request.method == 'POST':
        # Deleta o objeto do banco de dados.
        atracao.delete()
        # Redireciona para a lista de atrações.
        return redirect('atracoes_admin_index')

    # Se for uma requisição GET, apenas exibe a página de confirmação.
    context = {
        'atracao': atracao
    }
    return render(request, 'crud_app/atracoes_delete.html', context)

# View pública para listar todas as atrações.
def atracoes(request):
    atracoes_list = Atracao.objects.select_related('cidade', 'categoria').all()
    categorias = Categoria.objects.all()
    cidades = Cidade.objects.all()
    
    context = {
        'atracoes': atracoes_list,
        'categorias': categorias,
        'cidades': cidades,
    }
    return render(request, 'crud_app/atracoes.html', context)

def mapa(request):
    """
    Busca todas as atrações, cidades e categorias para popular os filtros e o mapa.
    """
    # Busca todos os dados necessários para o mapa e seus filtros.
    atracoes_list = Atracao.objects.select_related('cidade', 'categoria').all()
    categorias = Categoria.objects.all()
    cidades = Cidade.objects.all()

    # Monta o contexto com os dados para o template.
    context = {
        'atracoes': atracoes_list,
        'categorias': categorias,
        'cidades': cidades,
    }
    return render(request, 'crud_app/mapa.html', context)

def sobre(request):
    # Simplesmente renderiza a página 'sobre'.
    return render(request, 'crud_app/sobre.html')

def contato(request):
    # Simplesmente renderiza a página de 'contato'.
    return render(request, 'crud_app/contato.html')

def cadastro(request):
    # Se o formulário de cadastro foi enviado.
    if request.method == 'POST':
        # Coleta os dados do formulário.
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validação para garantir que campos essenciais não estão vazios.
        if not full_name or not email or not password:
            return render(request, 'crud_app/cadastro.html', {'error': 'Por favor, preencha todos os campos obrigatórios.'})

        # Cria um username único baseado no primeiro nome e na contagem de usuários.
        username = full_name.lower().split()[0] + str(User.objects.count() + 1)

        # Garante que o username seja único, adicionando um sufixo numérico se necessário.
        while User.objects.filter(username=username).exists():
             username += str(User.objects.count() + 1)
             
        # Verifica se o e-mail já está em uso.
        if User.objects.filter(email=email).exists():
            return render(request, 'crud_app/cadastro.html', {'error': 'Este e-mail já está cadastrado.'})


        # Tenta criar o novo usuário no banco de dados.
        try:
            # `create_user` é usado para garantir que a senha seja salva com hash de segurança.
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Adiciona o nome completo ao campo `first_name`.
            user.first_name = full_name
            user.save()

            # Autentica e faz o login do usuário recém-criado automaticamente.
            user_auth = authenticate(request, username=username, password=password)
            if user_auth is not None:
                auth_login(request, user_auth)
                return redirect('index') 
            
        except Exception as e:
            # Em caso de falha na criação
            return render(request, 'crud_app/cadastro.html', {'error': f'Erro interno: Não foi possível criar a conta. Detalhe: {e}'})

    # Se a requisição for GET, apenas mostra a página de cadastro.
    return render(request, 'crud_app/cadastro.html')

def login(request):
    # Se o formulário de login foi enviado.
    if request.method == 'POST':
        # Coleta os dados do formulário. O campo pode ser email ou username.
        username_or_email = request.POST.get('email') # O template envia 'email'
        password = request.POST.get('password')

        # Tenta encontrar o usuário pelo e-mail fornecido.
        user_match = None
        try:
            user_match = User.objects.get(email=username_or_email)
            username_to_auth = user_match.username
        except User.DoesNotExist:
            # Se não encontrar por e-mail, assume que o que foi digitado é o username.
            username_to_auth = username_or_email
        
        # Tenta autenticar o usuário com o username e a senha.
        user = authenticate(request, username=username_to_auth, password=password)

        # Se a autenticação for bem-sucedida.
        if user is not None:
            # Inicia a sessão para o usuário.
            auth_login(request, user)
            # Redireciona para a página inicial.
            return redirect('index')
        else: # Se a autenticação falhar.
            return render(request, 'crud_app/login.html', {'error': 'Credenciais inválidas.'})
            
    return render(request, 'crud_app/login.html')

def logout_view(request):
    """
    Encerra a sessão do usuário e o redireciona para a página inicial.
    """
    # Desloga o usuário da sessão atual.
    auth_logout(request)
    return redirect('index')

# ----------------------------------------------------------------------
# Views para o CRUD de usuários
# ----------------------------------------------------------------------
@staff_member_required
def usuarios_index(request):
    # Busca todos os usuários para listar na página de administração.
    usuarios = User.objects.all()
    return render(request, 'crud_app/usuarios/index.html', {'usuarios': usuarios})

@staff_member_required
def usuarios_create(request):
    # Se o formulário de criação de usuário foi enviado.
    if request.method == 'POST':
        # Cria um novo usuário usando `create_user` para hashear a senha.
        User.objects.create_user(
            username=request.POST['nome'].replace(" ", ""),
            email=request.POST.get('email', 'default@example.com'),
            password=request.POST['senha']
        )
        # Redireciona para a lista de usuários.
        return redirect('usuarios_index')
    return render(request, 'crud_app/usuarios/create.html')

@staff_member_required
def usuarios_edit(request, id):
    """
    Permite a edição dos dados básicos de um usuário (nome, email, status staff).
    A senha não deve ser alterada aqui, mas sim em uma view separada ou pelo Admin.
    """
    # Busca o usuário a ser editado.
    usuario = get_object_or_404(User, pk=id)
    error_message = None

    # Se o formulário de edição foi submetido.
    if request.method == 'POST':
        # Captura e atualiza os dados do objeto 'usuario' com as informações do formulário.
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        
        # Trata o campo 'is_staff', que é um booleano vindo de um checkbox.
        # O checkbox envia 'on' se marcado, e não envia nada se desmarcado.
        is_staff_checked = request.POST.get('is_staff') == 'on'
        usuario.is_staff = is_staff_checked

        try:
            # Salva as alterações no banco de dados.
            usuario.save()
            # Redireciona para a lista de usuários.
            return redirect('usuarios_index')
        except Exception as e:
            # Em caso de erro, armazena a mensagem para exibição.
            error_message = f'Erro ao salvar usuário: {e}'

    # Monta o contexto para enviar ao template.
    context = {
        'usuario': usuario,
        'error': error_message
    }
    return render(request, 'crud_app/usuarios/edit.html', context)

@staff_member_required
def usuarios_delete(request, id):
    # Busca o usuário a ser deletado.
    usuario = get_object_or_404(User, id=id)
    # Deleta o usuário. (Nota: esta view não tem uma etapa de confirmação).
    usuario.delete()
    # Redireciona para a lista de usuários.
    return redirect('usuarios_index')