function formatarData(dataIso) {
  const [ano, mes, dia] = dataIso.split('-');
  return `${dia}/${mes}/${ano}`;
}

async function cadastrar() {
  const numero = document.getElementById("numero").value;
  const nome = document.getElementById("nome").value;
  const data_inicial = document.getElementById("data").value;
  const dias = document.getElementById("dias").value;

  await fetch("/processos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ numero, nome, data_inicial, dias })
  });

  listar();
}

async function listar() {
  const resposta = await fetch("/processos");
  const resultado = await resposta.json();

  const processos = resultado.dados; // 🔥 AQUI está a correção

  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  processos.forEach(p => {
    lista.innerHTML += `
      <div>
        ${p.numero} - ${p.nome} - ${formatarData(p.prazo)}
        <button onclick="deletar('${p.numero}')">Deletar</button>
      </div>
    `;
  });
}

async function buscar() {
  const numero = document.getElementById("buscarNumero").value;

  const response = await fetch(`/processos/${numero}`);
  const result = await response.json();

  if (result.sucesso) {
    const p = result.dados;
    alert(`Processo encontrado:\nNúmero: ${p.numero}\nNome: ${p.nome}\nPrazo: ${formatarData(p.prazo)}`);
  } else {
    alert(result.erro);
  }
}

function mostrarMensagem(texto, tipo) {
  const div = document.getElementById("mensagem");
  div.textContent = texto;
  div.className = tipo;
  div.style.display = "block";

  setTimeout(() => {
    div.style.display = "none";
  }, 3000);
}

async function deletar(numero) {
  await fetch(`/processos/${numero}`, {
    method: "DELETE"
  });

  listar();
}