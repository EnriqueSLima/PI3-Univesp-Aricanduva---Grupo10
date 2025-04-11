function exibirLista() {
    // Esconde todas as listas
    document.querySelectorAll('.listagem').forEach(div => {
        div.style.display = 'none';
    });
    
    // Mostra a lista selecionada
    const modelo = document.getElementById('modelo').value;
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
        document.getElementById('modelo').value = modelo;
        exibirLista();
    }
});

function filtrarLista() {
    const atributo = document.getElementById('atributo').value;
    const termo = document.getElementById('termo').value;  // assumindo que tem um input para o termo
    
    if (atributo) {
        // Redirecionar ou fazer requisição AJAX com os parâmetros
        window.location.href = `?modelo={{ modelo }}&atributo=${atributo}&termo=${termo}`;
    }
}
