//#endregionFunção para exibir formularios
function exibirFormulario() {
    const modelo = document.getElementById('modelo').value;
    const formularios = document.querySelectorAll('.formulario-cadastro');
    
    // Esconde todos os formulários
    formularios.forEach(formulario => formulario.style.display = 'none');
    
    // Exibe o formulário correspondente ao valor selecionado, se houver
    if (modelo) {
        const formSelecionado = document.getElementById(`form-${modelo}`);
        if (formSelecionado) {
            formSelecionado.style.display = 'block';
        }
    }
}