from django import forms
from .models import Aluno, Livro, Editora, Categoria, Emprestimo

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'ra', 'sexo', 'ativo']  # Campos do modelo a serem incluídos no formulário
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome'}),
            'ra': forms.TextInput(attrs={'placeholder': 'Digite o RA'}),
            'sexo': forms.Select(choices=Aluno.SEXO_CHOICES),  # Para garantir que o campo 'sexo' seja exibido como um select
            'ativo': forms.Select(choices=Editora.ATIVO_CHOICES),
        }

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['tombo', 'registro', 'autor', 'titulo', 'procedencia', 'exemplar', 
                  'colecao', 'edicao', 'ano', 'vol', 'editora', 'observacao', 'aquisicao']
        widgets = {
            'tombo': forms.DateInput(format='%d/%m/%Y', attrs={
                'type': 'date', 'placeholder': 'Selecione a data do tombo'}),
            'registro': forms.NumberInput(attrs={
                'placeholder': 'Digite o registro', 'min': '1'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Digite o(a) autor(a)'}),
            'titulo': forms.TextInput(attrs={'placeholder': 'Digite o título'}),
            'procedencia': forms.TextInput(attrs={'placeholder': 'Digite a procedência'}),
            'exemplar': forms.NumberInput(attrs={'placeholder': 'Digite o exemplar', 'min': '1'}),
            'colecao': forms.TextInput(attrs={'placeholder': 'Digite a coleção'}),
            'edicao': forms.TextInput(attrs={'placeholder': 'Digite a edição'}),
            'ano': forms.NumberInput(attrs={'placeholder': 'Digite o ano', 'min': '1000', 'max': '2100'}),
            'vol': forms.NumberInput(attrs={'placeholder': 'Digite o volume', 'min': '1'}),
            'editora': forms.TextInput(attrs={'placeholder': 'Digite a editora'}),
            'observacao': forms.Textarea(attrs={'placeholder': 'Digite as observações', 'rows': 3}),
            'aquisicao': forms.Select(choices=Livro.AQUISICAO_CHOICES),
        }


class EditoraForm(forms.ModelForm):
    class Meta:
        model = Editora
        fields = ['nome', 'email', 'fone', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite o email'}),
            'fone': forms.TextInput(attrs={
                'placeholder': 'Digite DDD seguido do telefone, ex: 11945678345',
                'pattern': r'\d{10,11}',  # Aceita 10 a 11 dígitos
                'title': 'Digite o número no formato DDD + telefone, ex: 11945678345'
            }),
            'ativo': forms.Select(choices=Editora.ATIVO_CHOICES),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['tipo']
        widgets = {
            'tipo': forms.TextInput(attrs={'placeholder': 'Digite a categoria'})
        }

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['aluno', 'livro']  # Campos que o usuário irá preencher no formulário (o resto é calculado automaticamente)
        widgets = {
            'aluno': forms.Select(attrs={}),  # Campo para selecionar o aluno
            'livro': forms.Select(attrs={}),  # Campo para selecionar o livro
            'ativo': forms.Select(choices=Editora.ATIVO_CHOICES),

        }