from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Aluno, Livro, Emprestimo, Editora, Categoria

# Registrando os modelos
admin.site.register(Usuario, UserAdmin)
admin.site.register(Aluno)
admin.site.register(Livro)
admin.site.register(Emprestimo)
admin.site.register(Editora)
admin.site.register(Categoria)
