// Função que mostra as abas de empréstimo

function exibirAbaEmprestimo(modelo) {
    const formularios = document.querySelectorAll('.formulario-emprestimo');
    const abas = document.querySelectorAll('.aba-btn');
    
    // Esconde todos os formulários e remove classe 'ativa' das abas
    formularios.forEach(form => form.style.display = 'none');
    abas.forEach(aba => aba.classList.remove('active'));
    
    // Exibe o formulário correspondente e marca a aba como ativa
    if (modelo) {
        const formSelecionado = document.getElementById(`form-${modelo}`);
        const abaSelecionada = document.getElementById(`aba-${modelo}`);
        
        if (formSelecionado) {
            formSelecionado.style.display = 'block';
        }
        if (abaSelecionada) {
            abaSelecionada.classList.add('active');
        }
    }
        // Atualizar a URL sem recarregar a página
        const url = new URL(window.location.href);
        url.searchParams.set('modelo', modelo);
        // Limpar os parâmetros de busca quando mudar de aba
        window.history.pushState({}, '', url);
}

// Opcional: Mostrar a primeira aba por padrão ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.href);
    const modelo = urlParams.get('modelo') || 'novo'; // Padrão 'novo' se não especificado
    exibirAbaEmprestimo(modelo); // Ou qualquer outro padrão que desejar
});