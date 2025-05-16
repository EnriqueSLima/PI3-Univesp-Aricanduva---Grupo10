from django import forms
from .models import Usuario, Aluno, Livro, Editora, Emprestimo
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ["username", "email", "password1", "password2"]

class BaseModelForm(forms.ModelForm):
    # Classe Base para herança de usuário nos outros formulários
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
        fields = ['nome', 'data_nasc', 'sexo', 'ra']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o Nome'}),
            'data_nasc': forms.DateInput(format='%d/%m/%Y', attrs={
                'type': 'date', 'placeholder': 'Selecione a Data de Nacimento.'}),
            'sexo': forms.Select(choices=Aluno.SEXO_CHOICES),
            'ra': forms.TextInput(attrs={'placeholder': 'Digite o RA'}),
        }

class LivroForm(BaseModelForm):
    class Meta:
        model = Livro
        fields = ['tombo', 'registro', 'autor', 'titulo', 'ano', 
                'edicao', 'vol', 'editora', 'categoria', 
                'exemplar', 'aquisicao', 'observacao']
        widgets = {
            'tombo': forms.DateInput(format='%d/%m/%Y', attrs={
                'type': 'date', 'placeholder': 'Selecione a data do Tombo'}),
            'registro': forms.NumberInput(attrs={
                'placeholder': 'Digite o Registro', 'min': '1'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Digite o(a) Autor(a)'}),
            'titulo': forms.TextInput(attrs={'placeholder': 'Digite o Título'}),
            'ano': forms.NumberInput(attrs={'placeholder': 'Digite o Ano', 'min': '1900', 'max': '2100'}),
            'edicao': forms.TextInput(attrs={'placeholder': 'Digite a Edição'}),
            'vol': forms.NumberInput(attrs={'placeholder': 'Digite o Volume', 'min': '1'}),
            'editora': forms.TextInput(attrs={'placeholder': 'Digite a Editora'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Digite a Categoria'}),
            'exemplar': forms.NumberInput(attrs={'placeholder': 'Quantidade de exemplares', 'min': '1'}),
            'aquisicao': forms.Select(choices=Livro.AQUISICAO_CHOICES),
            'observacao': forms.Textarea(attrs={'placeholder': 'Observações', 'rows': 3}),
        }

class EditoraForm(BaseModelForm):
    class Meta:
        model = Editora
        fields = ['nome', 'email', 'fone']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o Nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite o Email'}),
            'fone': forms.TextInput(attrs={
                'placeholder': 'Digite DDD seguido do telefone, ex: 11945678345',
                'pattern': r'\d{10,11}',
                'title': 'Digite o número no formato DDD + telefone, ex: 11945678345'
            }),
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