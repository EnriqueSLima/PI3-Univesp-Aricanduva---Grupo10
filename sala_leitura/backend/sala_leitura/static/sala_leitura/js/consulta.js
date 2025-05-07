/* 
function exibirLista(modelo) {
    // Esconde todas as listas e remove classe 'ativa' das abas
    document.querySelectorAll('.listagem').forEach(div => {
        div.style.display = 'none';
    });
    document.querySelectorAll('.aba-btn').forEach(btn => {
        btn.classList.remove('ativa');
    });
    
    // Mostra a lista selecionada e marca a aba como ativa
    if (modelo) {
        const listaSelecionada = document.getElementById('list-' + modelo);
        const abaSelecionada = document.getElementById('aba-' + modelo);
        
        if (listaSelecionada) {
            listaSelecionada.style.display = 'block';
        }
        if (abaSelecionada) {
            abaSelecionada.classList.add('ativa');
        }
        
        // Atualiza a URL sem recarregar a página
        window.history.pushState({}, '', `?modelo=${modelo}`);
        
        // Opcional: Carregar dados via AJAX
        // carregarDados(modelo);
    }
}

// Exibe a lista correta ao carregar a página com parâmetro modelo
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelo = urlParams.get('modelo');
    
    // Define um modelo padrão se nenhum estiver na URL
    const modeloInicial = modelo || 'livros';
    
    exibirLista(modeloInicial);
});

// Opcional: Lidar com o botão voltar/avançar do navegador
window.addEventListener('popstate', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelo = urlParams.get('modelo') || 'livros';
    exibirLista(modelo);
}); */


function exibirLista(modelo) {
    // Esconder todas as listagens
    document.querySelectorAll('.listagem').forEach(function(item) {
        item.style.display = 'none';
    });
    
    // Remover classe ativa de todos os botões
    document.querySelectorAll('.aba-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });
    
    // Mostrar a listagem selecionada
    document.getElementById('list-' + modelo).style.display = 'block';
    
    // Adicionar classe ativa ao botão clicado
    document.getElementById('aba-' + modelo).classList.add('active');
    
    // Atualizar a URL sem recarregar a página
    const url = new URL(window.location.href);
    url.searchParams.set('modelo', modelo);
    // Limpar os parâmetros de busca quando mudar de aba
    url.searchParams.delete('campo');
    url.searchParams.delete('busca');
    window.history.pushState({}, '', url);
}

// Ao carregar a página, mostra a aba correta
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelo = urlParams.get('modelo') || 'livros';
    exibirLista(modelo);
});