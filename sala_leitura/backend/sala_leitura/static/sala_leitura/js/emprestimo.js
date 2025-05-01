
function mostrarNovoEmprestimo() {
    document.getElementById("novo-emprestimo-form").style.display = "block";
    document.getElementById("emprestimos-ativos").style.display = "none";
    document.getElementById("historico-emprestimos").style.display = "none";
}

function mostrarEmprestimosAtivos() {
    document.getElementById("emprestimos-ativos").style.display = "block";
    document.getElementById("novo-emprestimo-form").style.display = "none";
    document.getElementById("historico-emprestimos").style.display = "none";
}

function mostrarHistoricoEmprestimos() {
    document.getElementById("emprestimos-ativos").style.display = "none";
    document.getElementById("novo-emprestimo-form").style.display = "none";
    document.getElementById("historico-emprestimos").style.display = "block";
}