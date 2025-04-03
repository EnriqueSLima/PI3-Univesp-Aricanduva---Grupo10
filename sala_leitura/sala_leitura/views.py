# Imports necessários
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm, AlunoForm, LivroForm, EditoraForm, CategoriaForm, EmprestimoForm
from .models import Usuario, Aluno, Livro, Editora, Categoria, Emprestimo
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import login, authenticate
from urllib.parse import urlencode

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
    categorias_count = Categoria.objects.filter(usuario=request.user).count()
    editoras_count = Editora.objects.filter(usuario=request.user).count()
    
    # Contagem de empréstimos
    emprestimos_count = Emprestimo.objects.filter(usuario=request.user).count()  # Total de empréstimos realizados
    emprestimos_ativos_count = Emprestimo.objects.filter(usuario=request.user, ativo=True).count()  # Empréstimos ativos

    # Passando as variáveis para o template
    return render(request, 'home_page.html', {
        'livros_count': livros_count,
        'alunos_count': alunos_count,
        'categorias_count': categorias_count,
        'editoras_count': editoras_count,
        'emprestimos_count': emprestimos_count,
        'emprestimos_ativos_count': emprestimos_ativos_count
    })


# View para a consultas
@login_required
def consulta(request):
    return render(request, 'consulta.html')

# View para a listar livros
@login_required
def lista_livros(request):
    filtro = request.GET.get('filtro')
    valor = request.GET.get('valor')
    livros = Livro.objects.filter(usuario=request.user)

    if filtro and valor:
        if filtro == 'registro':
            livros = livros.filter(registro__icontains=valor)
        elif filtro == 'autor':
            livros = livros.filter(autor__icontains=valor)
        elif filtro == 'titulo':
            livros = livros.filter(titulo__icontains=valor)
        elif filtro == 'editora':
            livros = livros.filter(editora__icontains=valor)
    
    return render(request, 'lista_livros.html', {'livros': livros})

# View para os detalhes do livro
def detalhes_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    return render(request, 'detalhes_livro.html', {'livro': livro})

# View para a listar alunos
@login_required
def lista_alunos(request):
    filtro = request.GET.get('filtro')
    valor = request.GET.get('valor')
    alunos = Aluno.objects.filter(usuario=request.user)
    is_sexo_filter = False  # Flag para identificar se o filtro é 'sexo'

    if filtro and valor:
        if filtro == 'nome':
            alunos = alunos.filter(nome__icontains=valor)
        elif filtro == 'ra':
            alunos = alunos.filter(ra__icontains=valor)
        elif filtro == 'sexo':
            alunos = alunos.filter(sexo__iexact=valor)
            is_sexo_filter = True  # Ativa a flag para o filtro de sexo

    return render(request, 'lista_alunos.html', {'alunos': alunos, 'is_sexo_filter': is_sexo_filter})

# View para a listar editoras
@login_required
def lista_editoras(request):
    busca_nome = request.GET.get('busca_nome')
    editoras = Editora.objects.filter(usuario=request.user)

    if busca_nome:
        editoras = editoras.filter(nome__icontains=busca_nome)
    
    return render(request, 'lista_editoras.html', {'editoras': editoras})

# View para a listar categorias
@login_required
def lista_categorias(request):
    busca_nome = request.GET.get('busca_nome')
    categorias = Categoria.objects.filter(usuario=request.user)

    if busca_nome:
        categorias = categorias.filter(tipo__icontains=busca_nome)
    
    return render(request, 'lista_categorias.html', {'categorias': categorias})

# View para a listar emprestimos
@login_required
def lista_emprestimos(request):
    filtro = request.GET.get('filtro')
    valor = request.GET.get('valor')
    
    # Inicia a consulta de empréstimos com devolução confirmada
    historicos = Emprestimo.objects.filter(usuario=request.user, data_devolucao__isnull=False)

    if filtro and valor:
        if filtro == 'aluno':
            historicos = historicos.filter(aluno__nome__icontains=valor)
        elif filtro == 'titulo':
            historicos = historicos.filter(livro__titulo__icontains=valor)
        elif filtro == 'data_devolucao':
            try:
                # Tenta filtrar por data de devolução se o valor for uma data válida
                data_devolucao = timezone.datetime.strptime(valor, "%d/%m/%Y").date()
                historicos = historicos.filter(data_devolucao=data_devolucao)
            except ValueError:
                pass  # Caso não seja uma data válida, não aplica filtro
    
    # Carrega todas as opções de alunos e livros para o filtro
    alunos = Aluno.objects.filter(usuario=request.user)
    livros = Livro.objects.filter(usuario=request.user)

    return render(request, 'lista_emprestimos.html', {
        'historicos': historicos,
        'alunos': alunos,
        'livros': livros,
        'filtro': filtro,
        'valor': valor
    })


@login_required
def cadastro(request):
    modelo = request.GET.get('modelo', 'alunos')  # Default para 'alunos' se não especificado

    # Inicializa formulários vazios com o request, para coletar o id so usuário
    form_livros = LivroForm(request=request)
    form_alunos = AlunoForm(request=request)
    form_editoras = EditoraForm(request=request)
    form_categorias = CategoriaForm(request=request)

    if request.method == 'POST':
        # Verifica qual formulário foi enviado
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
                
        elif modelo == 'categorias':
            form_categorias = CategoriaForm(request.POST, request=request)
            if form_categorias.is_valid():
                form_categorias.save()
                messages.success(request, 'Categoria cadastrada com sucesso!')
                return redirect(f"{reverse('cadastro')}?modelo={modelo}")

    # Passa todos os formulários e o modelo selecionado para o contexto
    context = {
        'form_livros': form_livros,
        'form_alunos': form_alunos,
        'form_editoras': form_editoras,
        'form_categorias': form_categorias,
        'modelo': modelo
    }
    return render(request, 'cadastro.html', context)

# View para emprestimos
@login_required
def emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empréstimo realizado com sucesso!')
            return redirect('emprestimo') 
    else:
        form = EmprestimoForm()

    # Filtra os empréstimos que ainda estão ativos
    emprestimos_ativos = Emprestimo.objects.filter(usuario=request.user, ativo=True)
    emprestimos_hist = Emprestimo.objects.filter(usuario=request.user)
    return render(request, 'emprestimo.html', {
        'form': form,
        'emprestimos': emprestimos_ativos,
        'historicos' : emprestimos_hist
    })

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

