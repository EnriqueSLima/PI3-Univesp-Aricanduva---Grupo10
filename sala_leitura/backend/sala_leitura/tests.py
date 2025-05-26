from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Usuario, Aluno, Livro, Editora, Emprestimo

class LivroModelTest(TestCase):

    def setUp(self):
        # Cria um usuário para testes
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    # --- TESTE QUE DEVE PASSAR --- #
    def test_criacao_livro_valido(self):
        livro = Livro.objects.create(
            registro=123,
            autor="Machado de Assis",
            titulo="Dom Casmurro",
            ano=1899,
            edicao="1ª Edição",
            editora="Editora A",
            exemplar=1,
            aquisicao='C',  # Compra
            usuario=self.usuario  # Associa ao usuário criado no setUp
        )
        # Verifica se o livro foi criado corretamente
        self.assertEqual(livro.titulo, "Dom Casmurro")
        self.assertEqual(livro.aquisicao, 'C')  # Checa a escolha (Compra)
        self.assertEqual(livro.usuario.username, 'testuser')  # Checa o usuário
    # --- TESTE QUE DEVE FALHAR --- #
    def test_registro_duplicado_falha(self):
        # Cria um livro com registro 123
        Livro.objects.create(
            registro=123,
            autor="Autor 1",
            titulo="Livro 1",
            edicao="1ª Edição",
            editora="Editora X",
            exemplar=1,
            aquisicao='D',  # Doação
            usuario=self.usuario
        )
        # Tenta criar outro livro com o MESMO registro (deve falhar)
        with self.assertRaises(Exception):  # Captura qualquer exceção
            Livro.objects.create(
                registro=123,  # Registro duplicado!
                autor="Autor 2",
                titulo="Livro 2",
                edicao="2ª Edição",
                editora="Editora Y",
                exemplar=2,
                aquisicao='T',  # Troca
                usuario=self.usuario
            )

class AlunoModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username='professor', password='testpass123')

    # --- TESTES QUE DEVEM PASSAR --- #
    def test_criacao_aluno_valido(self):
        aluno = Aluno.objects.create(
            nome="João Silva",
            data_nasc="2010-05-15",
            sexo='M',
            ra="20230001",
            usuario=self.usuario
        )
        self.assertEqual(aluno.__str__(), "João Silva")  # Testa __str__
        self.assertEqual(aluno.sexo, 'M')  # Checa choice

    # --- TESTES QUE DEVEM FALHAR --- #
    def test_ra_duplicado_falha(self):
        Aluno.objects.create(
            nome="Aluno 1", ra="20230001", sexo='F', usuario=self.usuario
        )
        with self.assertRaises(Exception):  # RA duplicado
            Aluno.objects.create(
                nome="Aluno 2", ra="20230001", sexo='M', usuario=self.usuario
            )

    def test_sexo_invalido_falha(self):
        with self.assertRaises(ValidationError):
            aluno = Aluno(
                nome="Aluno 3", ra="20230002", sexo='X', usuario=self.usuario  # Sexo inválido
            )
            aluno.full_clean()  # Força validação do modelo

class EmprestimoModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username='bibliotecario', password='testpass123')
        self.aluno = Aluno.objects.create(
            nome="Maria Oliveira", ra="20230002", sexo='F', usuario=self.usuario
        )
        self.livro = Livro.objects.create(
            registro=123, autor="Autor X", titulo="Livro Y", edicao="1ª",
            editora="Editora Z", exemplar=1, aquisicao='C', usuario=self.usuario
        )

    # --- TESTES QUE DEVEM PASSAR --- #
    def test_criacao_emprestimo_valido(self):
        emprestimo = Emprestimo.objects.create(
            aluno=self.aluno,
            livro=self.livro,
            usuario=self.usuario
        )
        self.assertTrue(emprestimo.ativo)  # Deve estar ativo ao criar

    # --- TESTES QUE DEVEM FALHAR --- #
    def test_emprestimo_sem_livro_falha(self):
        with self.assertRaises(Exception):  # Livro é obrigatório
            Emprestimo.objects.create(
                aluno=self.aluno,
                usuario=self.usuario
            )
