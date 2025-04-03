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

    ATIVO_CHOICES = [
        (True, 'Sim'),
        (False, 'Não'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    ra = models.CharField(max_length=20, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    ativo = models.BooleanField(default=True, choices=ATIVO_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='alunos')  # Novo campo

    def __str__(self):
        return self.nome

class Livro(models.Model):
    AQUISICAO_CHOICES = [
        ('C', 'Compra'),
        ('D', 'Doação'),
        ('T', 'Troca'),
    ]
    
    id = models.AutoField(primary_key=True)
    tombo = models.DateTimeField(null=True, blank=True)
    registro = models.IntegerField(unique=True)
    autor = models.CharField(max_length=500)
    titulo = models.CharField(max_length=500)
    procedencia = models.CharField(max_length=500)
    exemplar = models.PositiveIntegerField()
    colecao = models.CharField(max_length=500)
    edicao = models.CharField(max_length=50)
    ano = models.PositiveIntegerField(null=True, blank=True)
    vol = models.PositiveIntegerField(null=True, blank=True)
    editora = models.CharField(max_length=500)
    categoria = models.CharField(max_length=500, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    aquisicao = models.CharField(max_length=1, choices=AQUISICAO_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='livros')  # Novo campo
    
    def __str__(self):
        return f'{self.titulo} ({self.autor})'

class Editora(models.Model):
    ATIVO_CHOICES = [
        (True, 'Sim'),
        (False, 'Não'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=500)
    email = models.CharField(max_length=50)
    fone = models.CharField(max_length=11)
    ativo = models.BooleanField(default=True, choices=ATIVO_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='editoras')  # Novo campo

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='categorias')  # Novo campo

    def __str__(self):
        return self.tipo

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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='emprestimos')  # Novo campo

    def __str__(self):
        return f'{self.aluno.nome} - {self.livro.titulo}'

    def salvar(self, *args, **kwargs):
        if self.data_devolucao and self.data_devolucao <= timezone.now():
            self.ativo = False
        else:
            self.ativo = True
        super(Emprestimo, self).save(*args, **kwargs)

