from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.db.models import Q

from .models import Usuario, Aluno, Livro, Editora, Emprestimo
from .forms import UsuarioForm, AlunoForm, LivroForm, EditoraForm, EmprestimoForm

# View para home_page
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing_page')
    else:
        form = UsuarioForm()
    return render(request, 'cadastrar_usuario.html', {'form': form})

# View para a landing page
def landing_page(request):
    return render(request, 'landing_page.html')

# View para a home_page
@login_required(login_url='landing_page')
def home_page(request):
    # Contagem de livros, alunos, categorias e editoras
    livros_count = Livro.objects.filter(usuario=request.user).count()
    alunos_count = Aluno.objects.filter(usuario=request.user).count()
    editoras_count = Editora.objects.filter(usuario=request.user).count()
    
    # Contagem de empréstimos
    emprestimos_count = Emprestimo.objects.filter(usuario=request.user).count()  # Total de empréstimos realizados
    emprestimos_ativos_count = Emprestimo.objects.filter(usuario=request.user, ativo=True).count()  # Empréstimos ativos

    # Passando as variáveis para o template
    return render(request, 'home_page.html', {
        'livros_count': livros_count,
        'alunos_count': alunos_count,
        'editoras_count': editoras_count,
        'emprestimos_count': emprestimos_count,
        'emprestimos_ativos_count': emprestimos_ativos_count
    })

# View para cadastros dos itens
@login_required
def cadastro(request):
    modelo = request.GET.get('modelo', 'alunos')  # Default para 'alunos' se não especificado

    # Inicializa formulários vazios com o request, para coletar o id so usuário
    form_livros = LivroForm(request=request)
    form_alunos = AlunoForm(request=request)
    form_editoras = EditoraForm(request=request)

    if request.method == 'POST':
        # Verifica qual formulário foi enviado
        # !!!   Necessário Refatorar  !!!
        if modelo == 'alunos':
            form_alunos = AlunoForm(request.POST, request=request)
            if form_alunos.is_valid():
                form_alunos.save()
                messages.success(request, 'Aluno cadastrado com sucesso!')
                return redirect(f"{reverse('cadastro')}?modelo={modelo}")
                
        elif modelo == 'livros':
            form_livros = LivroForm(request.POST, request=request)
            if form_livros.is_valid():
                form_livros.save()
                messages.success(request, 'Livro cadastrado com sucesso!')
                return redirect(f"{reverse('cadastro')}?modelo={modelo}")
                
        elif modelo == 'editoras':
            form_editoras = EditoraForm(request.POST, request=request)
            if form_editoras.is_valid():
                form_editoras.save()
                messages.success(request, 'Editora cadastrada com sucesso!')
                return redirect(f"{reverse('cadastro')}?modelo={modelo}")
                
    # Passa todos os formulários e o modelo selecionado para o contexto
    context = {
        'form_livros': form_livros,
        'form_alunos': form_alunos,
        'form_editoras': form_editoras,
        'modelo': modelo
    }
    return render(request, 'cadastro.html', context)

# View para a consultas
@login_required
def consulta(request):
    modelo = request.GET.get('modelo', 'livros')
    
    # Dados base filtrados por usuário
    dados = {
        'livros': Livro.objects.filter(usuario=request.user),
        'alunos': Aluno.objects.filter(usuario=request.user),
        'editoras': Editora.objects.filter(usuario=request.user),
    }

    # Aplicar filtros específicos para cada modelo
    campo = request.GET.get('campo', '')
    busca = request.GET.get('busca', '')
    
    if busca:
        if modelo == 'livros':
            dados['livros'] = filtrar_livros(dados['livros'], campo, busca)
        elif modelo == 'alunos':
            dados['alunos'] = filtrar_alunos(dados['alunos'], campo, busca)
        elif modelo == 'editoras':
            dados['editoras'] = filtrar_editoras(dados['editoras'], campo, busca)

    context = {
        'modelo': modelo,
        **dados,
        'request': request
    }
    
    return render(request, 'consulta.html', context)

# Funções auxiliares para filtros
def filtrar_livros(queryset, campo, busca):
    if campo == 'titulo':
        return queryset.filter(titulo__icontains=busca)
    elif campo == 'registro':
        return queryset.filter(registro__icontains=busca)
    elif campo == 'autor':
        return queryset.filter(autor__icontains=busca)
    elif campo == 'editora':
        return queryset.filter(editora__nome__icontains=busca)
    elif campo == 'ano':
        return queryset.filter(ano__icontains=busca)
    else:
        return queryset.filter(
        # Busca em todos os campos se nenhum campo específico foi selecionado
            Q(titulo__icontains=busca) |
            Q(registro__icontains=busca) |
            Q(autor__icontains=busca) |
            Q(editora__nome__icontains=busca) |
            Q(ano__icontains=busca)
        )

def filtrar_alunos(queryset, campo, busca):
    if campo == 'nome':
        return queryset.filter(nome__icontains=busca)
    elif campo == 'ra':
        return queryset.filter(ra__icontains=busca)
    elif campo == 'sexo':
        return queryset.filter(sexo__icontains=busca)
    else:
        return queryset.filter(
            Q(nome__icontains=busca) |
            Q(ra__icontains=busca) |
            Q(sexo__icontains=busca)
        )
    
def filtrar_editoras(queryset, campo, busca):
    if campo == 'nome':
        return queryset.filter(nome__icontains=busca)
    elif campo == 'email':
        return queryset.filter(email__icontains=busca)
    # ... outros filtros para alunos
    else:
        return queryset.filter(
            Q(nome__icontains=busca) |
            Q(email__icontains=busca)
            # ... outros campos
        )

# View para emprestimos

@login_required
def emprestimo(request):
    # Lógica para POST (novo empréstimo)
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empréstimo realizado com sucesso!')
            return redirect('emprestimo') 
    else:
        form = EmprestimoForm(request=request)

    # Filtros para empréstimos ativos
    emprestimos_ativos = Emprestimo.objects.filter(
        usuario=request.user, 
        ativo=True
    ).select_related('livro', 'aluno')
    
    # Filtros para histórico
    emprestimos_hist = Emprestimo.objects.filter(
        usuario=request.user
    ).select_related('livro', 'aluno')
    
    # Parâmetros de filtro para ativos (vêm da URL)
    campo_ativo = request.GET.get('campo_ativo', '')
    busca_ativo = request.GET.get('busca_ativo', '')
    
    if busca_ativo:
        emprestimos_ativos = filtrar_emprestimos(emprestimos_ativos, campo_ativo, busca_ativo)
    
    # Parâmetros de filtro para histórico
    campo_hist = request.GET.get('campo', '')
    busca_hist = request.GET.get('busca', '')
    
    if busca_hist:
        emprestimos_hist = filtrar_emprestimos(emprestimos_hist, campo_hist, busca_hist)

    return render(request, 'emprestimo.html', {
        'form': form,
        'emprestimos': emprestimos_ativos,
        'historicos': emprestimos_hist,
        'campo_ativo': campo_ativo,
        'busca_ativo': busca_ativo,
        'request': request
    })

def filtrar_emprestimos(queryset, campo, busca):
    if campo == 'livro':
        return queryset.filter(livro__titulo__icontains=busca)
    elif campo == 'aluno':
        return queryset.filter(aluno__nome__icontains=busca)
    elif campo == 'data_emprestimo':
        return queryset.filter(data_emprestimo__icontains=busca)
    elif campo == 'data_devolucao':
        return queryset.filter(data_devolucao__icontains=busca)
    else:
        # Busca em todos os campos se nenhum específico foi selecionado
        return queryset.filter(
            Q(livro__titulo__icontains=busca) |
            Q(aluno__nome__icontains=busca) |
            Q(data_emprestimo__icontains=busca) |
            Q(data_devolucao__icontains=busca)
        )

# Função para devolver livro
@login_required
def devolver_livro(request, emprestimo_id):
    # Obter o empréstimo com o ID fornecido ou 404 se não existir
    emprestimo = get_object_or_404(Emprestimo.objects.filter(usuario=request.user, ativo=True), id=emprestimo_id)

    # Define a data_devolucao para a data atual e desativa o empréstimo
    emprestimo.data_devolucao = timezone.now().date()
    emprestimo.ativo = False
    emprestimo.save()
    messages.success(request, 'Devolução realizada com sucesso!')

    return redirect('emprestimo')

# View para os detalhes do livro
def detalhes_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    return render(request, 'detalhes_livro.html', {'livro': livro})

# View para os detalhes do(a) aluno(a)
def detalhes_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    return render(request, 'detalhes_aluno.html', {'aluno': aluno})

# View para os detalhes da editora
def detalhes_editora(request, id):
    editora = get_object_or_404(Editora, id=id)
    return render(request, 'detalhes_editora.html', {'editora': editora})
