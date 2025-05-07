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