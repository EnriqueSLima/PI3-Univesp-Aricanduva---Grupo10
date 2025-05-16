// Função que mostra as abas de empréstimo

function exibirAbaDados(modelo) {
    const formularios = document.querySelectorAll('.formulario-dados');
    const abas = document.querySelectorAll('.aba-btn');
    
    // Esconde todos os formulários e remove classe 'ativa' das abas
    formularios.forEach(form => form.style.display = 'none');
    abas.forEach(aba => aba.classList.remove('active'));
    
    // Exibe o formulário correspondente e marca a aba como ativa
    if (modelo) {
        const formSelecionado = document.getElementById(`data-${modelo}`);
        const abaSelecionada = document.getElementById(`aba-${modelo}`);
        
        if (formSelecionado) {
            formSelecionado.style.display = 'block';
        }
        if (abaSelecionada) {
            abaSelecionada.classList.add('active');
        }
    }
}
// Opcional: Mostrar a primeira aba por padrão ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    exibirAbaDados('livros'); // Ou qualquer outro padrão que desejar
});