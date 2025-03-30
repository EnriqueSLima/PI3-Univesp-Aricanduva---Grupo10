from django.db import models
from django.utils import timezone
from datetime import timedelta

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

    id = models.AutoField(primary_key=True)  # Campo id auto incrementável
    nome = models.CharField(max_length=255)  # Nome do aluno
    ra = models.CharField(max_length=20, unique=True)  # RA do aluno, único
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)  # Sexo do aluno
    ativo = models.BooleanField(default=True, choices= ATIVO_CHOICES)  # Status do aluno (ativo ou não)
    
    def __str__(self):
        return self.nome

class Livro(models.Model):
    AQUISICAO_CHOICES = [
        ('C', 'Compra'),
        ('D', 'Doação'),
        ('T', 'Troca'),
    ]
    
    id = models.AutoField(primary_key=True)  # ID automático
    tombo = models.DateTimeField(null=True, blank=True)  # Tombo como data (sem horas e minutos)
    registro = models.IntegerField(unique=True)  # Registro como número inteiro
    autor = models.CharField(max_length=500)  # Autor do livro
    titulo = models.CharField(max_length=500)  # Título do livro
    procedencia = models.CharField(max_length=500)  # Procedência do livro
    exemplar = models.PositiveIntegerField()  # Número do exemplar
    colecao = models.CharField(max_length=500)  # Coleção do livro
    edicao = models.CharField(max_length=50)  # Edição do livro
    ano = models.PositiveIntegerField(null=True, blank=True)  # Ano de publicação
    vol = models.PositiveIntegerField(null=True, blank=True)  # Volume
    editora = models.CharField(max_length=500)  # Editora do livro
    categoria = models.CharField(max_length=500, null=True, blank=True)  # Editora do livro
    observacao = models.TextField(null=True, blank=True)  # Observações
    aquisicao = models.CharField(max_length=1, choices=AQUISICAO_CHOICES)  # Tipo de aquisição
    
    def __str__(self):
        return f'{self.titulo} ({self.autor})'

class Editora(models.Model):
    ATIVO_CHOICES = [
        (True, 'Sim'),
        (False, 'Não'),
    ]

    id = models.AutoField(primary_key=True)  # ID automático
    nome = models.CharField(max_length=500)  # Nome do aluno
    email = models.CharField(max_length=50)
    fone = models.CharField(max_length=11)
    ativo = models.BooleanField(default=True,  choices= ATIVO_CHOICES)  # Status do aluno (ativo ou não)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)  # ID automático
    tipo = models.CharField(max_length=255)  # Nome do aluno

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

    def __str__(self):
        return f'{self.aluno.nome} - {self.livro.titulo}'

    # Método para atualizar o status 'ativo' automaticamente
    def salvar(self, *args, **kwargs):
        if self.data_devolucao and self.data_devolucao <= timezone.now():
            self.ativo = False  # Torna inativo se a data de devolução foi atingida
        else:
            self.ativo = True  # Torna ativo se a devolução não aconteceu ainda
        super(Emprestimo, self).save(*args, **kwargs)  # Salva normalmente
