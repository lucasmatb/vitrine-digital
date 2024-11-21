let edicao = false;
const botaoEditar = document.querySelector(".botao-editar");
const body = document.querySelector("body");
const botaoExcluir = document.querySelectorAll(".botao-excluir");
const modalConfirmacao = document.querySelector(".modal-confirmacao");

const botaoSim = document.querySelector(".botao-sim");
const botaoCancelar = document.querySelector(".botao-cancelar");

const todosCards = document.querySelector(".todos-cards");
// console.log(modalConfirmacao);

botaoEditar.addEventListener("click", () => {
    if (edicao === false) {
        edicao = true;
        body.classList.add("modo-edicao");
        console.log(body.classList);
        botaoEditar.textContent = "Concluir";

        abrirModalConfirmacao();
    } else {
        edicao = false;
        body.classList.remove("modo-edicao");
        botaoEditar.textContent = "Editar";
    }
});

function abrirModalConfirmacao() {
    botaoExcluir.forEach((b) => {
        b.addEventListener("click", () => {
            modalConfirmacao.classList.add("aberto");

            botaoSim.addEventListener("click", () => {
                // REMOVER DO BANCO DE DADOS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1 LUCAAASSSASSAAAAAAA
                todosCards.removeChild(b.parentElement);
                modalConfirmacao.classList.remove("aberto");
            });

            botaoCancelar.addEventListener("click", () => {
                modalConfirmacao.classList.remove("aberto");
                console.log("foi");
            });
        });
    });
}
