// Para os alertas das páginas
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert-overlay');
    
    alerts.forEach(alert => {
        // Mostra o alerta com animação
        setTimeout(() => {
            alert.classList.add('show');
        }, 50);
        
        // Fecha automaticamente após 5 segundos
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 300); // Tempo para a animação completar
        }, 1200);
    });
});


/* function exibirLista(tipo) {
    // Esconder todas as listagens primeiro
    document.querySelectorAll('.listagem').forEach(function(el) {
        el.style.display = 'none';
    });
    
    // Mostrar apenas a listagem selecionada
    document.getElementById('list-' + tipo).style.display = 'block';
    
    // Remover a classe 'active' de todos os botões
    document.querySelectorAll('.aba-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });
    
    // Adicionar a classe 'active' apenas ao botão clicado
    document.getElementById('aba-' + tipo).classList.add('active');
    
    // Alterar a cor do fundo da div listagens
    document.querySelector('.listagens').classList.add('active');
    
    // Salvar a aba ativa no localStorage para persistir entre páginas
    localStorage.setItem('abaAtiva', tipo);
}

// Ao carregar a página, verificar se há uma aba ativa salva
document.addEventListener('DOMContentLoaded', function() {
    const abaAtiva = localStorage.getItem('abaAtiva') || 'livros';
    exibirLista(abaAtiva);
});
 */