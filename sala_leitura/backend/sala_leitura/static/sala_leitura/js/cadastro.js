//Função para exibir formularios
function exibirFormulario() {
    const modelo_cad = document.getElementById('modelo').value;
    const formularios = document.querySelectorAll('.formulario-cadastro');
    
    // Esconde todos os formulários
    formularios.forEach(formulario => formulario.style.display = 'none');
    
    // Exibe o formulário correspondente ao valor selecionado, se houver
    if (modelo_cad) {
        const formSelecionado = document.getElementById(`form-${modelo_cad}`);
        if (formSelecionado) {
            formSelecionado.style.display = 'block';
        }
    }
}

//Função para exibir formularios
//function exibirLista() {
//    const model_list = document.getElementById('model').value;
//    const listas = document.querySelectorAll('.listagem');
//    
//    // Esconde todos os formulários
//    listas.forEach(lista => lista.style.display = 'none');
//    
//    // Exibe o formulário correspondente ao valor selecionado, se houver
//    if (model_list) {
//        const listSelecionado = document.getElementById(`list-${model_list}`);
//        if (listSelecionado) {
//            listSelecionado.style.display = 'block';
//        }
//    }
//}