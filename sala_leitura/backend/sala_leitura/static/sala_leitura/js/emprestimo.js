// Função para extrair o parâmetro 'tab' da URL
function getCurrentTab() {
    const params = new URLSearchParams(window.location.search);
    return params.get('tab'); // 'novo' como padrão
}

// Função para mostrar a aba correta
function showCorrectTab() {
    const tab = getCurrentTab();
    
    if (tab === 'ativos') {
        document.getElementById('novo-emprestimo-form').style.display = 'none';
        document.getElementById('emprestimos-ativos').style.display = 'block';
        document.getElementById('historico-emprestimos').style.display = 'none';
    } else if (tab === 'historicos') {
        document.getElementById('novo-emprestimo-form').style.display = 'none';
        document.getElementById('emprestimos-ativos').style.display = 'none';
        document.getElementById('historico-emprestimos').style.display = 'block';
    } else {
        document.getElementById('novo-emprestimo-form').style.display = 'block';
        document.getElementById('emprestimos-ativos').style.display = 'none';
        document.getElementById('historico-emprestimos').style.display = 'none';
    }
}

// Modifica as funções das abas para atualizar a URL
function mostrarNovoEmprestimo() {
    const params = new URLSearchParams(window.location.search);
    params.set('tab', 'novo');
    window.history.pushState({}, '', `?${params.toString()}`);
    showCorrectTab();
}

function mostrarEmprestimosAtivos() {
    const params = new URLSearchParams(window.location.search);
    params.set('tab', 'ativos');
    window.history.pushState({}, '', `?${params.toString()}`);
    showCorrectTab();
}

function mostrarHistoricoEmprestimos() {
    const params = new URLSearchParams(window.location.search);
    params.set('tab', 'historicos');
    window.history.pushState({}, '', `?${params.toString()}`);
    showCorrectTab();
}

// Ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    showCorrectTab();
    
    // Adicione este evento para lidar com o botão de voltar/avançar do navegador
    window.addEventListener('popstate', function() {
        showCorrectTab();
    });
});