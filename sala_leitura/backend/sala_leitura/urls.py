from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from . import views

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
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # Funcionalidade nativa Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Funcionalidade nativa Django
    path('signin/', views.cadastrar_usuario, name='signin'),
    path('', landing_page, name='landing_page'),    
    path('home/', home_page, name='home_page'),
    path('consulta/', consulta, name='consulta'),
    path('detalhes_livro/<int:id>/', detalhes_livro, name='detalhes_livro'),
    path('detalhes_aluno/<int:id>/', detalhes_aluno, name='detalhes_aluno'),
    path('detalhes_editora/<int:id>/', detalhes_editora, name='detalhes_editora'),
    path('cadastro/', cadastro, name='cadastro'),
    path('emprestimo/', emprestimo, name='emprestimo'),
    path('emprestimo/devolver/<int:emprestimo_id>/', devolver_livro, name='devolver_livro'), # Função que devolve o livro
]
