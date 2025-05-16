from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Herda todos os campos padrão do User (username, email, password, etc.)
    def __str__(self):
        return self.username

class Aluno(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    data_nasc = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    ra = models.CharField(max_length=20, unique=True)
    # Relaciona o cadastro a um único usuário.
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='alunos')

    def __str__(self):
        return self.nome

class Livro(models.Model):
    AQUISICAO_CHOICES = [
        ('C', 'Compra'),
        ('D', 'Doação'),
        ('T', 'Troca'),
    ]
    
    id = models.AutoField(primary_key=True)
    registro = models.IntegerField(unique=True)
    autor = models.CharField(max_length=50)
    titulo = models.CharField(max_length=100)
    ano = models.PositiveIntegerField(null=True, blank=True)
    edicao = models.CharField(max_length=50)
    vol = models.PositiveIntegerField(null=True, blank=True)
    editora = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    exemplar = models.PositiveIntegerField()
    aquisicao = models.CharField(max_length=1, choices=AQUISICAO_CHOICES)
    observacao = models.TextField(null=True, blank=True)
    # Relaciona o cadastro a um único usuário.
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='livros')
    
    def __str__(self):
        return f'{self.titulo} ({self.autor})'

class Editora(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    fone = models.CharField(max_length=15)
    # Relaciona o cadastro a um único usuário.
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='editoras')

    def __str__(self):
        return self.nome

# Função que define a data prevista de devolução (caso necessário)
def data_devolucao_default():
    return timezone.now() + timezone.timedelta(days=7)  # Exemplo: 7 dias após o empréstimo

class Emprestimo(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    livro = models.ForeignKey('Livro', on_delete=models.CASCADE)
    data_emprestimo = models.DateField(default=timezone.now)
    data_prev = models.DateField(default=data_devolucao_default)
    data_devolucao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    # Relaciona o cadastro a um único usuário.
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='emprestimos')

    def __str__(self):
        return f'{self.aluno.nome} - {self.livro.titulo}'

    def salvar(self, *args, **kwargs):
        if self.data_devolucao and self.data_devolucao <= timezone.now():
            self.ativo = False
        else:
            self.ativo = True
        super(Emprestimo, self).save(*args, **kwargs)

