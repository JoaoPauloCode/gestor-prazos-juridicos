async function cadastrar() {
  const numero = document.getElementById("numero").value;
  const nome = document.getElementById("nome").value;
  const data = document.getElementById("data").value;
  const dias = document.getElementById("dias").value;

  const response = await fetch("http://127.0.0.1:5000/processos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      numero,
      nome,
      data_inicial: data,
      dias: parseInt(dias)
    })
  });

  const result = await response.json();

  if (response.ok) {
  mostrarMensagem("Processo cadastrado com sucesso!", "sucesso");
  } else {
    mostrarMensagem(result.erro || "Erro ao cadastrar", "erro");
  }

  listar();
}

async function listar() {
  const response = await fetch("http://127.0.0.1:5000/processos");
  const processos = await response.json();

  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  processos.forEach(p => {
    const item = document.createElement("li");

    item.innerHTML = `
      <strong>${p.numero}</strong> - ${p.nome}<br>
      Prazo: ${p.prazo}
      <br><br>
      <button onclick="deletar('${p.numero}')">Deletar</button>
    `;

    lista.appendChild(item);
  });
}

async function buscar() {
  const numero = document.getElementById("buscarNumero").value;

  const response = await fetch(`http://127.0.0.1:5000/processos/${numero}`);
  const result = await response.json();

  alert(JSON.stringify(result));
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
  const confirmar = confirm("Tem certeza que deseja deletar?");

  if (!confirmar) return;

  const response = await fetch(`http://127.0.0.1:5000/processos/${numero}`, {
    method: "DELETE"
  });

  const result = await response.json();
  const processos = result.dados;

  if (response.ok) {
    mostrarMensagem("Processo deletado com sucesso!", "sucesso");
    listar();
  } else {
    mostrarMensagem(result.erro || "Erro ao deletar", "erro");
  }
}