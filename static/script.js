const feriados = [
  "2026-01-01",
  "2026-02-16",
  "2026-02-17",
  "2026-02-18",
  "2026-04-03",
  "2026-04-05",
  "2026-04-21",
  "2026-05-01",
  "2026-06-04",
  "2026-09-07",
  "2026-10-12",
  "2026-11-02",
  "2026-11-15",
  "2026-11-20",
  "2026-12-25"
];

function calcularPrazo(dataInicial, dias) {
  let data = new Date(dataInicial);
  let adicionados = 0;

  while (adicionados < dias) {
    data.setDate(data.getDate() + 1);

    const diaSemana = data.getDay();
    const dataISO = data.toISOString().split("T")[0];

    const ehFimDeSemana = (diaSemana === 0 || diaSemana === 6);
    const ehFeriado = feriados.includes(dataISO);

    if (!ehFimDeSemana && !ehFeriado) {
      adicionados++;
    }
  }

  return data.toISOString().split("T")[0];
}

function formatarData(dataIso) {
  const [ano, mes, dia] = dataIso.split('-');
  return `${dia}/${mes}/${ano}`;
}

async function cadastrar() {
  const numero = document.getElementById("numero").value;
  const nome = document.getElementById("nome").value;
  const data_inicial = document.getElementById("data").value;
  const dias = document.getElementById("dias").value;

 
  const prazoFinal = calcularPrazo(data_inicial, parseInt(dias));

  await fetch("/processos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      numero,
      nome,
      prazo: prazoFinal
    })
  });

  listar();
  mostrarMensagem("Processo cadastrado com sucesso!", "sucesso");
}

async function listar() {
  const resposta = await fetch("/processos");
  const resultado = await resposta.json();

  const processos = resultado.dados;

  const lista = document.getElementById("lista"); 
  lista.innerHTML = ""; 

  processos.forEach(p => {
    const dataFormatada = formatarData(p.prazo);

    lista.innerHTML += `
      <div class="processo">
        <span>${p.numero} - ${p.nome} - ${dataFormatada}</span>
        <button class="btn-delete" onclick="deletar('${p.numero}')">
          Excluir
        </button>
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
    mostrarMensagem(
      `Processo: ${p.numero} - ${p.nome} - ${formatarData(p.prazo)}`,
      "sucesso"
    );
  } else {
    mostrarMensagem(result.erro, "erro");
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
  if (!confirm("Tem certeza que deseja excluir?")) return;

  await fetch(`/processos/${numero}`, {
    method: "DELETE"
  });

  listar();
  mostrarMensagem("Processo excluído com sucesso!", "sucesso");
}

window.onload = listar;