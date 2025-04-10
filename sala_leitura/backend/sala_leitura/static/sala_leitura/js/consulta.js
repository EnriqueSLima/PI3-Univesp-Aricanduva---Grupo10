function exibirLista() {
    // Esconde todas as listas
    document.querySelectorAll('.listagem').forEach(div => {
        div.style.display = 'none';
    });
    
    // Mostra a lista selecionada
    const modelo = document.getElementById('model').value;
    if (modelo) {
        document.getElementById('list-' + modelo).style.display = 'block';
        // Atualiza a URL sem recarregar a página
        window.history.pushState({}, '', `?modelo=${modelo}`);
    }
}

// Exibe a lista correta ao carregar a página com parâmetro modelo
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelo = urlParams.get('modelo');
    if (modelo) {
        document.getElementById('model').value = modelo;
        exibirLista();
    }
});