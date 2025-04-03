let fonteTamanho = 1; // Tamanho da fonte inicial (1 = normal)
let modoContrasteAtivo = false;

function ajustarFonte(acao) {
    // Seleciona os elementos que terão o tamanho da fonte alterado
    const elementos = [
        document.body,
        document.getElementById('page-head'),
        document.getElementById('page-footer'),
        document.getElementById('navbar'),
        ...document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, div')
    ];

    // Aumenta ou diminui o tamanho da fonte com base na ação
    if (acao === 'aumentar') {
        fonteTamanho += 0.1;
    } else if (acao === 'diminuir') {
        fonteTamanho -= 0.1;
    }

    // Aplica o novo tamanho de fonte nos elementos selecionados
    elementos.forEach(elemento => {
        elemento.style.fontSize = fonteTamanho + 'em';
    });
}

function mudarContraste() {
    // Seleciona os elementos que terão o contraste alterado
    const elementos = [
        document.body,
        document.getElementById('page-head'),
        document.getElementById('page-footer'),
        document.getElementById('navbarNav'),
        ...document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, div')
    ];

    // Alterna entre o modo normal e o de alto contraste
    if (modoContrasteAtivo) {
        // Remove a classe de alto contraste
        elementos.forEach(elemento => {
            elemento.classList.remove('alto-contraste');
        });
    } else {
        // Adiciona a classe de alto contraste
        elementos.forEach(elemento => {
            elemento.classList.add('alto-contraste');
        });
    }

    modoContrasteAtivo = !modoContrasteAtivo; // Alterna o estado do contraste
}

// Função para alternar o modo de alto contraste
function toggleContraste() {
    document.body.classList.toggle('alto-contraste');
    
    // Salva o estado do alto contraste no cookie
    if (document.body.classList.contains('alto-contraste')) {
        document.cookie = "altoContraste=ativo; path=/; max-age=" + 60*60*24*365; // expira em 1 ano
    } else {
        document.cookie = "altoContraste=inativo; path=/; max-age=" + 60*60*24*365;
    }
}

// Função para verificar o estado do alto contraste ao carregar a página
window.onload = function() {
    let cookies = document.cookie.split(';');
    let contrasteCookie = cookies.find(cookie => cookie.trim().startsWith('altoContraste='));

    if (contrasteCookie && contrasteCookie.split('=')[1] === 'ativo') {
        document.body.classList.add('alto-contraste');
    }
};