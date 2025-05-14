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

