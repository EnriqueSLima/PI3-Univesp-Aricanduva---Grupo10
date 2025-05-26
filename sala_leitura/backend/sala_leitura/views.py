from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from .models import Usuario, Aluno, Livro, Editora, Emprestimo
from .forms import UsuarioForm, AlunoForm, LivroForm, EditoraForm, EmprestimoForm

# VIEW PARA LANDING-PAGE
def landing_page(request):
    return render(request, 'landing_page.html')

# VIEW DE CADASTRO DE USUÁRIOS
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

# USUÁRIO PRECISA ESTAR LOGADO PARA ACESSAR AS PROXIMAS VIEWS

# VIEW PARA HOME_PAGE
@login_required(login_url='landing_page')
def home_page(request):
    # Contagem de livros, alunos, categorias e editoras
    livros_count = Livro.objects.filter(usuario=request.user).distinct().count()
    alunos_count = Aluno.objects.filter(usuario=request.user).distinct().count()
    categorias_count = Livro.objects.filter(usuario=request.user).values('categoria').distinct().count()
    editoras_count = Livro.objects.filter(usuario=request.user).values('editora').distinct().count()
    # Contagem de empréstimos
    emprestimos_count = Emprestimo.objects.filter(usuario=request.user).count()  # Total de empréstimos realizados
    emprestimos_ativos_count = Emprestimo.objects.filter(usuario=request.user, ativo=True).count()  # Empréstimos ativos

    # Consulta para pegar o top 5 categorias
    top_categorias = (
        Livro.objects
        .filter(usuario=request.user)
        .values('categoria') 
        .annotate(total=Count('id'))
        .order_by('-total')[:5]  # Apenas as 5 categorias com mais livros
    )

    # Extrai labels e valores
    categorias = [item['categoria'] for item in top_categorias]
    cat_quantidades = [item['total'] for item in top_categorias]

    categorias = categorias[::-1]          # Inverte a ordem das categorias
    cat_quantidades = cat_quantidades[::-1]  # Inverte a ordem dos valores

    # Cria o gráfico
    plt.figure(figsize=(10, 5))
    bars = plt.barh(categorias, cat_quantidades, color='lightgreen')
    plt.title('Top 5 Categorias com Mais Livros')

    # Remove bordas para um visual mais limpo
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Salva o gráfico em uma imagem base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    cat_grafico = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Consulta para pegar o top 5 editoras
    top_editoras = (
        Livro.objects
        .filter(usuario=request.user)
        .values('editora')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # Extrai labels e valores
    editoras = [item['editora'] for item in top_editoras]
    edit_quantidades = [item['total'] for item in top_editoras]

    editoras = editoras[::-1]
    edit_quantidades = edit_quantidades[::-1]

    # Cria o gráfico
    plt.figure(figsize=(10, 5))
    plt.barh(editoras, edit_quantidades, color='green')
    plt.title('Top 5 Editoras com Mais Livros')

    # Remove bordas para um visual mais limpo
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Converte para imagem
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    edit_grafico = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Passando as variáveis para o template
    return render(request, 'home_page.html', {
        'livros_count': livros_count,
        'alunos_count': alunos_count,
        'editoras_count': editoras_count,
        'categorias_count': categorias_count,
        'emprestimos_count': emprestimos_count,
        'emprestimos_ativos_count': emprestimos_ativos_count,
        'cat_grafico' : cat_grafico,
        'edit_grafico' : edit_grafico,
    })

# VIEW PARA CADASTROS
@login_required
def cadastro(request):
    modelo = request.GET.get('modelo', 'livros')  # Default para 'livros' se não especificado

    # Inicializa formulários vazios com o request, para coletar o id so usuário
    form_livros = LivroForm(request=request)
    form_alunos = AlunoForm(request=request)
    form_editoras = EditoraForm(request=request)

    if request.method == 'POST':
        # Verifica qual formulário foi enviado
        # !Necessário Refatorar  
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

# VIEW PARA CONSULTAS
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

# FUNÇÕES AUXILIARES PARA FILTROS DE CONSULTA
# FILTRAR LIVROS
def filtrar_livros(queryset, campo, busca):
    if campo == 'titulo':
        return queryset.filter(titulo__icontains=busca)
    elif campo == 'registro':
        return queryset.filter(registro__icontains=busca)
    elif campo == 'autor':
        return queryset.filter(autor__icontains=busca)
    elif campo == 'editora':
        return queryset.filter(editora__icontains=busca)
    elif campo == 'ano':
        return queryset.filter(ano__icontains=busca)
    else:
        return queryset.filter(
        # Busca em todos os campos se nenhum campo específico foi selecionado
            Q(titulo__icontains=busca) |
            Q(registro__icontains=busca) |
            Q(autor__icontains=busca) |
            Q(editora__icontains=busca) |
            Q(ano__icontains=busca)
        )

# FILTRAR ALUNOS
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

# FILTRAR EDITORAS
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

# VIEW PARA EMPRÉSTIMOS
@login_required
def emprestimo(request):
    modelo = request.GET.get('modelo', 'novo')

    # Gerar um novo empréstimo
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
    
    # Parâmetros de filtro para histórico (vêm da URL)
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

# FUNÇÃO AUXILIAR DEVOLVER EMPRÉSTIMO ATIVO
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

# FUNÇÃO AUXILIAR PARA FILTRAR HISTÓRICO DE EMPRÉSTIMOS
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

# VIEW PARA DETALHES DO LIVRO
@login_required
def detalhes_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    return render(request, 'detalhes_livro.html', {'livro': livro})

# VIEW PARA EDITAR LIVRO
@login_required
def editar_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('detalhes_livro', id=id)
    else:
        form = LivroForm(instance=livro)
    return render(request, 'editar_livro.html', {'form': form, 'livro': livro})

# VIEW PARA EXCLUIR LIVRO
@login_required
def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('consulta')  # Redireciona para a página de consulta
    # Esta parte não será alcançada devido ao modal, mas é bom ter
    return redirect('detalhes_livro', pk=livro.pk)

# VIEW PARA DETALHES DO(A) ALUNO
@login_required
def detalhes_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    return render(request, 'detalhes_aluno.html', {'aluno': aluno})

# VIEW PARA EDITAR ALUNO
@login_required
def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno(a) atualizado(a) com sucesso!')
            return redirect('detalhes_aluno', id=id)
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'editar_aluno.html', {'form': form, 'aluno': aluno})

# VIEW PARA EXCLUIR ALUNO
@login_required
def excluir_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        return redirect('consulta')  # Redireciona para a página de consulta
    # Esta parte não será alcançada devido ao modal, mas é bom ter
    return redirect('detalhes_aluno', pk=aluno.pk)

# VIEW PARA DETALHES DA EDITORA
@login_required
def detalhes_editora(request, id):
    editora = get_object_or_404(Editora, id=id)
    return render(request, 'detalhes_editora.html', {'editora': editora})

# VIEW PARA EDITAR EDITORA
@login_required
def editar_editora(request, id):
    editora = get_object_or_404(Editora, id=id)
    if request.method == 'POST':
        form = EditoraForm(request.POST, instance=editora)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editora atualizada com sucesso!')
            return redirect('detalhes_editora', id=id) 
    else:
        form = EditoraForm(instance=editora)
    return render(request, 'editar_editora.html', {'form': form, 'editora': editora})

# VIEW PARA EXCLUIR EDITORA
@login_required
def excluir_editora(request, pk):
    editora = get_object_or_404(Editora, pk=pk)
    if request.method == 'POST':
        editora.delete()
        messages.success(request, 'Editora excluída com sucesso!')
        return redirect('consulta')  # Redireciona para a página de consulta
    # Esta parte não será alcançada devido ao modal, mas é bom ter
    return redirect('detalhes_editora', pk=editora.pk)