from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from . import views

# IMPORTA OS NOMES EM VIEWS.PY PARA OS CONTEXTOS
from .views import (
    cadastrar_usuario,
    landing_page,
    home_page,
    consulta,
    cadastro,
    emprestimo,
    devolver_livro,
    detalhes_livro,
    detalhes_aluno,
    detalhes_editora,
    editar_livro,
    excluir_livro
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # Funcionalidade nativa Django (autenticar)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Funcionalidade nativa Django (desautenticar)
    path('signin/', views.cadastrar_usuario, name='signin'), # Funcionalidade nativa Django (cadastrar)
    path('', landing_page, name='landing_page'),    
    path('home/', home_page, name='home_page'),
    path('cadastro/', cadastro, name='cadastro'),
    path('consulta/', consulta, name='consulta'),
    path('emprestimo/', emprestimo, name='emprestimo'),
    path('emprestimo/devolver/<int:emprestimo_id>/', devolver_livro, name='devolver_livro'), # Função que devolve o livro
    path('detalhes_livro/<int:id>/', detalhes_livro, name='detalhes_livro'),
    path('livro/<int:id>/editar/', views.editar_livro, name='editar_livro'),
    path('livro/<int:pk>/excluir/', views.excluir_livro, name='excluir_livro'), # Função que exclui livro
    path('detalhes_aluno/<int:id>/', detalhes_aluno, name='detalhes_aluno'),
    path('aluno/<int:id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('aluno/<int:pk>/excluir/', views.excluir_aluno, name='excluir_aluno'), # Função que exclui aluno
    path('detalhes_editora/<int:id>/', detalhes_editora, name='detalhes_editora'),
    path('editora/<int:id>/editar/', views.editar_editora, name='editar_editora'),
    path('editora/<int:pk>/excluir/', views.excluir_editora, name='excluir_editora'), # Função que exclui editora
]
