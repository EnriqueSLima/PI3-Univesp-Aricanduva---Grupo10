from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Aluno, Livro, Editora, Categoria, Emprestimo

class TestModels(TestCase):

    def test_aluno_creation(self):
        aluno = Aluno.objects.create(
            nome="João da Silva",
            ra="123456789",
            sexo="M",
            ativo=True
        )
        self.assertEqual(aluno.nome, "João da Silva")
        self.assertEqual(aluno.ra, "123456789")
        self.assertEqual(aluno.sexo, "M")
        self.assertTrue(aluno.ativo)
        self.assertIsInstance(aluno, Aluno)

    def test_livro_creation(self):
        livro = Livro.objects.create(
            registro=123456,
            autor="Autor Teste",
            titulo="Livro de Teste",
            procedencia="Compra",
            exemplar=1,
            colecao="Coleção Teste",
            edicao="1ª Edição",
            ano=2024,
            vol=1,
            editora="Editora Teste",
            categoria="Ficção",
            aquisicao="C"
        )
        self.assertEqual(livro.registro, 123456)
        self.assertEqual(livro.titulo, "Livro de Teste")
        self.assertEqual(livro.autor, "Autor Teste")
        self.assertEqual(livro.procedencia, "Compra")
        self.assertEqual(livro.aquisicao, "C")
        self.assertIsInstance(livro, Livro)

    def test_editora_creation(self):
        editora = Editora.objects.create(
            nome="Editora Teste",
            email="contato@editora.com",
            fone="12345678901",
            ativo=True
        )
        self.assertEqual(editora.nome, "Editora Teste")
        self.assertEqual(editora.email, "contato@editora.com")
        self.assertEqual(editora.fone, "12345678901")
        self.assertTrue(editora.ativo)
        self.assertIsInstance(editora, Editora)

    def test_categoria_creation(self):
        categoria = Categoria.objects.create(
            tipo="Ficção"
        )
        self.assertEqual(categoria.tipo, "Ficção")
        self.assertIsInstance(categoria, Categoria)

    def test_emprestimo_creation(self):
        aluno = Aluno.objects.create(
            nome="Maria Oliveira",
            ra="987654321",
            sexo="F",
            ativo=True
        )
        livro = Livro.objects.create(
            registro=654321,
            autor="Outro Autor",
            titulo="Outro Livro",
            procedencia="Doação",
            exemplar=2,
            colecao="Coleção A",
            edicao="2ª Edição",
            ano=2023,
            vol=2,
            editora="Editora A",
            categoria="Drama",
            aquisicao="D"
        )
        emprestimo = Emprestimo.objects.create(
            aluno=aluno,
            livro=livro,
            data_emprestimo=timezone.now(),
            data_prev=timezone.now() + timedelta(days=7),
            ativo=True
        )
        self.assertEqual(emprestimo.aluno, aluno)
        self.assertEqual(emprestimo.livro, livro)
        self.assertIsNotNone(emprestimo.data_emprestimo)
        self.assertIsNotNone(emprestimo.data_prev)
        self.assertTrue(emprestimo.ativo)

    def test_emprestimo_status_on_devolucao(self):
        aluno = Aluno.objects.create(
            nome="Carlos Souza",
            ra="111223344",
            sexo="M",
            ativo=True
        )
        livro = Livro.objects.create(
            registro=111222,
            autor="Autor X",
            titulo="Livro X",
            procedencia="Troca",
            exemplar=3,
            colecao="Coleção X",
            edicao="3ª Edição",
            ano=2022,
            vol=3,
            editora="Editora X",
            categoria="Suspense",
            aquisicao="T"
        )
        # Empréstimo com data de devolução no passado
        emprestimo = Emprestimo.objects.create(
            aluno=aluno,
            livro=livro,
            data_emprestimo=timezone.now() - timedelta(days=10),
            data_prev=timezone.now() - timedelta(days=3),
            data_devolucao=timezone.now() - timedelta(days=1),  # Devolução no passado
            ativo=True
        )
        # Verificar se o status do empréstimo foi alterado para inativo
        emprestimo.save()  # Necessário para que o método `salvar()` seja chamado
        self.assertFalse(emprestimo.ativo)

    def test_emprestimo_status_on_active(self):
        aluno = Aluno.objects.create(
            nome="Ana Costa",
            ra="2233445566",
            sexo="F",
            ativo=True
        )
        livro = Livro.objects.create(
            registro=223344,
            autor="Autor Y",
            titulo="Livro Y",
            procedencia="Compra",
            exemplar=4,
            colecao="Coleção Y",
            edicao="4ª Edição",
            ano=2021,
            vol=4,
            editora="Editora Y",
            categoria="Mistério",
            aquisicao="C"
        )
        # Empréstimo com data de devolução ainda não registrada
        emprestimo = Emprestimo.objects.create(
            aluno=aluno,
            livro=livro,
            data_emprestimo=timezone.now(),
            data_prev=timezone.now() + timedelta(days=7),
            ativo=True
        )
        self.assertTrue(emprestimo.ativo)

    def test_invalid_ra_on_aluno(self):
        aluno = Aluno.objects.create(
            nome="Ricardo Silva",
            ra="12345",  # RA inválido, menos de 20 caracteres
            sexo="M",
            ativo=True
        )
        with self.assertRaises(Exception):
            aluno.full_clean()  # Espera-se que um erro de validação ocorra

    def test_unique_ra(self):
        aluno1 = Aluno.objects.create(
            nome="Lucas Lima",
            ra="54321",
            sexo="M",
            ativo=True
        )
        with self.assertRaises(Exception):
            aluno2 = Aluno.objects.create(
                nome="Ana Oliveira",
                ra="54321",  # RA duplicado
                sexo="F",
                ativo=True
            )
            aluno2.full_clean()  # Deve lançar erro de duplicação de RA

