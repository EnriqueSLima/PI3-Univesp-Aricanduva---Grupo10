from django import forms
from .models import Usuario, Aluno, Livro, Editora, Categoria, Emprestimo
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ["username", "email", "password1", "password2"]

class BaseModelForm(forms.ModelForm):
    """Classe base para herança dos outros formulários"""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and hasattr(self.request, 'user'):
            instance.usuario = self.request.user
        if commit:
            instance.save()
        return instance

class AlunoForm(BaseModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'ra', 'sexo', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome'}),
            'ra': forms.TextInput(attrs={'placeholder': 'Digite o RA'}),
            'sexo': forms.Select(choices=Aluno.SEXO_CHOICES),
            'ativo': forms.Select(choices=Aluno.ATIVO_CHOICES),
        }

class LivroForm(BaseModelForm):
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

class EditoraForm(BaseModelForm):
    class Meta:
        model = Editora
        fields = ['nome', 'email', 'fone', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite o email'}),
            'fone': forms.TextInput(attrs={
                'placeholder': 'Digite DDD seguido do telefone, ex: 11945678345',
                'pattern': r'\d{10,11}',
                'title': 'Digite o número no formato DDD + telefone, ex: 11945678345'
            }),
            'ativo': forms.Select(choices=Editora.ATIVO_CHOICES),
        }

class CategoriaForm(BaseModelForm):
    class Meta:
        model = Categoria
        fields = ['tipo']
        widgets = {
            'tipo': forms.TextInput(attrs={'placeholder': 'Digite a categoria'})
        }

class EmprestimoForm(BaseModelForm):
    class Meta:
        model = Emprestimo
        fields = ['aluno', 'livro']
        widgets = {
            'aluno': forms.Select(attrs={}),
            'livro': forms.Select(attrs={}),
        }

    def save(self, commit=True):
        emprestimo = super().save(commit=False)
        
        # Define automaticamente o usuário e o status ativo
        if self.request and hasattr(self.request, 'user'):
            emprestimo.usuario = self.request.user
        emprestimo.ativo = True
        
        if commit:
            emprestimo.save()
        return emprestimo