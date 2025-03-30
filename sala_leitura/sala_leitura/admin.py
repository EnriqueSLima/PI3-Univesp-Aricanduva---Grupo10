from django.contrib import admin
from .models import Aluno, Livro, Emprestimo, Editora, Categoria

# Registrando os modelos
admin.site.register(Aluno)
admin.site.register(Livro)
admin.site.register(Emprestimo)
admin.site.register(Editora)
admin.site.register(Categoria)
