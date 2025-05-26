import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sala_leitura.models import Aluno, Livro

User = get_user_model()

class Command(BaseCommand):
    help = 'Importa dados de CSV para os modelos Aluno e Livro'

    def handle(self, *args, **options):
        # 1. Obter o usuário admin (ou outro usuário para associar)
        try:
            usuario = User.objects.get(username='Nagila')  # Altere para o usuário desejado
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuário admin não encontrado! Crie um usuário primeiro.'))
            return

        # 2. Importar Alunos
        self.importar_alunos(usuario)
        
        # 3. Importar Livros
        self.importar_livros(usuario)

    def importar_alunos(self, usuario):
        caminho_csv = '../../csv/alunos_exemplo.csv'  # Ajuste o caminho
        
        with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            
            for linha in leitor:
                try:
                    # Converter data (DD/MM/AAAA para YYYY-MM-DD)
                    data_nasc = datetime.strptime(linha['data_nasc'], '%d/%m/%Y').date()
                    
                    Aluno.objects.create(
                        nome=linha['nome'],
                        data_nasc=data_nasc,
                        sexo=linha['sexo'],
                        ra=linha['ra'],
                        usuario=usuario
                    )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Erro ao importar aluno {linha['nome']}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f'Importação de alunos concluída!'))

    def importar_livros(self, usuario):
        caminho_csv = '../../csv/livros_exemplo.csv'  # Ajuste o caminho
        
        with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            
            for linha in leitor:
                try:
                    # Tratar exemplar (converte float para int se necessário)
                    exemplar = linha['exemplar']
                    if isinstance(exemplar, str) and '.' in exemplar:
                        exemplar = int(float(exemplar))  # Converte "1.0" para 1
                    else:
                        exemplar = int(exemplar)
                    
                    Livro.objects.create(
                        registro=linha['registro'],
                        autor=linha['autor'],
                        titulo=linha['titulo'],
                        ano=int(linha['ano']) if linha['ano'] else None,
                        edicao=linha['edicao'],
                        vol=int(linha['vol']) if linha['vol'] else None,
                        editora=linha['editora'],
                        categoria=linha['categoria'],
                        exemplar=exemplar,  # Usando o valor tratado
                        aquisicao=linha['aquisicao'],
                        observacao=linha['observacao'],
                        usuario=usuario
                    )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f"Erro ao importar livro {linha.get('titulo', '')}: {str(e)}"
                    ))
        
        self.stdout.write(self.style.SUCCESS(f'Importação de livros concluída!'))
