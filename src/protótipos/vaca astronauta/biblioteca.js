/**
 * Este código é apenas um exemplo didático.
 * Cada grupo precisará desenvolver sua própria biblioteca para incorporar
 * todas as funções necessárias.
 */

const listaDeObjetos = [];
let ultimaPos = 0;
let ultimaTecla = -1;
const largura = 1080;
const altura = 720;
const figurasValidas = ["quadrado", "circulo"];

const canvas = document.getElementById("tutorial");
const divImagens = document.getElementById("imagens"); // id da div que armazena imagens

// Espera ms milisegundos. Deve ser chamada como: await esperar(ms), dentro de uma função async
function esperar(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Inicializa o canvas com uma cor de fundo
function inicializar_com_cor(cor) {
    canvas.style.borderWidth = "1px";
    canvas.style.borderStyle = "solid";
    canvas.style.borderColor = "grey";
    canvas.style.backgroundColor = cor;
}

// Inicializa o canvas com uma imagem de fundo
function inicializar_com_imagem(arq) {
    let ctx = canvas.getContext("2d");
    let img = new Image();
    img.src = arq;
    img.onload = function() {
        ctx.drawImage(img, 0, 0, largura, altura);
    };
}

// Limpa todos os objetos do canvas
function limparTela() {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, largura, altura);
}

// desenha um objeto de um determinado tipo: "quadrado" ou "circulo"
function desenharFigura(tipo, cor, x, y, tamanho) {
    const ctx = canvas.getContext("2d");
    if (tipo === "quadrado") {
        ctx.fillStyle = cor;
        ctx.fillRect(x, y, tamanho, tamanho);
    } else if (tipo === "circulo") {
        ctx.beginPath();
        ctx.fillStyle = cor;
        ctx.arc(x, y, tamanho, 0, 2 * Math.PI);
        ctx.fill();
    }
}

// cria uma figura geométrica e retorna o seu id (posição no array de objetos)
function criar_figura(tipo, cor, x, y, tamanho) {
    if (figurasValidas.includes(tipo)) {
        listaDeObjetos[ultimaPos] = { tipo, cor, x, y, tamanho };
        desenharFigura(tipo, cor, x, y, tamanho);
        ultimaPos++;
        return ultimaPos - 1;
    } else {
        return -1;
    }
}

// reaproveita um id e associa outra figura a ele
function redefinir_figura(id, tipo, cor, x, y, tamanho) {
    if (id >= 0 && id < listaDeObjetos.length && figurasValidas.includes(tipo)) {
        listaDeObjetos[id] = { tipo, cor, x, y, tamanho };
        limparTela();
        redesenharTodos();
        desenharFigura(tipo, cor, x, y, tamanho);
        return true;
    } else {
        return false;
    }
}

// desenha a imagem no canvas na coordenada x, y
function desenharImagem(x, y, url) {
    const ctx = canvas.getContext("2d");
    const img = divImagens.querySelector(`img[src='${url}']`);
    if (img) {
        let imgWidth = img.width;
        let imgHeight = img.height;

        // Redimensiona a imagem se for maior que 400x400
        if (imgWidth > 400 || imgHeight > 400) {
            const scaleFactor = Math.min(400 / imgWidth, 400 / imgHeight);
            imgWidth *= scaleFactor;
            imgHeight *= scaleFactor;
        }

        ctx.drawImage(img, x, y, imgWidth, imgHeight);
    }
}

// cria uma imagem pela url e retorna o seu id
function criar_imagem(url, x, y) {
    const img = document.createElement("img");
    img.src = url;
    divImagens.appendChild(img);
    listaDeObjetos[ultimaPos] = { "tipo": "imagem", "x": x, "y": y, "url": url }

    // precisa aguardar um pouco para que a figura de fato esteja na div
    async function aguardaParaExibir() {
        await esperar(50);
        desenharImagem(x, y, url);
    };
    aguardaParaExibir();

    ultimaPos++;
    return ultimaPos - 1;
}

// reaproveita um id e associa outra imagem a ele
function redefinir_imagem(id, url, x, y) {
    if (id >= 0 && id < listaDeObjetos.length) {
        listaDeObjetos[id] = { tipo: "imagem", x, y, url };
        limparTela();
        redesenharTodos();
        desenharImagem(x, y, url);
        return true;
    } else {
        return false;
    }
}

// move um objeto no sentido raster, de acordo com o deslocamento dx e dy (podem ser inteiros positivos ou negativos)
function mover(id, dx, dy) {
    if (listaDeObjetos[id] != null) {
        obj = listaDeObjetos[id];
        limparTela();
        obj.x += dx;
        obj.y += dy;
        if (obj.tipo == "imagem")
            desenharImagem(obj.x, obj.y, obj.url)
        else
            desenharFigura(obj.tipo, obj.cor, obj.x, obj.y, obj.tamanho);
        redesenharTodosComExcecao(id);
    }
}

// Detecta colisão entre dois objetos. Trata todos eles como retângulos, para facilitar a implementação
function colidiu(id1, id2) {
    if (id1 >= 0 && id2 >= 0 && id1 < listaDeObjetos.length && id2 < listaDeObjetos.length) {
        const obj1 = listaDeObjetos[id1];
        const obj2 = listaDeObjetos[id2];
        let w1, w2, h1, h2;

        if (obj1.tipo === "imagem") {
            const img1 = divImagens.querySelector(`img[src='${obj1.url}']`);
            w1 = img1.width;
            h1 = img1.height;
        } else {
            w1 = h1 = obj1.tamanho;
        }

        if (obj2.tipo === "imagem") {
            const img2 = divImagens.querySelector(`img[src='${obj2.url}']`);
            w2 = img2.width;
            h2 = img2.height;
        } else {
            w2 = h2 = obj2.tamanho;
        }

        return obj1.x < obj2.x + w2 && obj1.x + w1 > obj2.x && obj1.y < obj2.y + h2 && obj1.y + h1 > obj2.y;
    }
    return false;
}

function mostrar(msg) {
<<<<<<<< HEAD:src/jogos/vaca astronauta/biblioteca.js
    document.addEventListener('DOMContentLoaded', function() {
        const displayArea = document.getElementById("mensagem");
    if (displayArea) {
        displayArea.textContent += msg;
        console.log(`Mensagem mostrada: ${msg}`);
    } else {
        console.log("Elemento de mensagem não encontrado.");
    }
    });
========
    document.getElementById("mensagem").textContent = msg;
>>>>>>>> gerador-funcional:src/jogo/biblioteca.js
    
}

function consultar() {
    const valor = ultimaTecla;
    ultimaTecla = -1;
    return valor;
}

function destacar(id) {
    const ctx = canvas.getContext("2d");
    ctx.save();
    ctx.globalAlpha = 0.5;
    limparTela();
    redesenharTodosComExcecao(id);
    ctx.globalAlpha = 1;
    const obj = listaDeObjetos[id];
    if (obj.tipo === "imagem") {
        desenharImagem(obj.x, obj.y, obj.url);
    } else {
        desenharFigura(obj.tipo, obj.cor, obj.x, obj.y, obj.tamanho);
    }
    ctx.restore();
}

function reverter_destaque() {
    limparTela();
    redesenharTodos();
}

function tocar(arq) {
    const audio = new Audio(arq);
    audio.play().catch(error => {
        console.error("Erro ao tentar tocar o áudio:", error);
    });
}

async function ler_numero(msg) {
    while (true) {
        const input = prompt(msg);
        const numero = parseInt(input, 10);
        if (!isNaN(numero)) {
            return numero;
        }
    }
}

async function ler_binario(msg) {
    return confirm(msg);
}

function ler() {
    return new Promise(resolve => {
        function onKeyDown(event) {
<<<<<<<< HEAD:src/jogos/vaca astronauta/biblioteca.js
            if (event.key === "ArrowUp") {
                document.removeEventListener("keydown", onKeyDown);
                resolve(1); // 1 representa a tecla seta para cima
            }
        }
        document.addEventListener("keydown", onKeyDown);
========
            switch (event.key) {
                case "ArrowUp":
                    resolve(1);
                    break;
                case "ArrowDown":
                    resolve(2);
                    break;
                case "ArrowLeft":
                    resolve(3);
                    break;
                case "ArrowRight":
                    resolve(4);
                    break;
                case " ":
                    resolve(5);
                    break;
                case "Enter":
                    resolve(6);
                    break;
                default:
                    return; // Ignore other keys
            }
            document.removeEventListener("keydown", onKeyDown);
            document.removeEventListener("mousedown", onMouseDown);
            document.removeEventListener("mousemove", onMouseMove);
        }

        function onMouseDown(event) {
            switch (event.button) {
                case 0:
                    resolve(7);
                    break;
                case 2:
                    resolve(8);
                    break;
                default:
                    return; // Ignore other mouse buttons
            }
            document.removeEventListener("keydown", onKeyDown);
            document.removeEventListener("mousedown", onMouseDown);
            document.removeEventListener("mousemove", onMouseMove);
        }

        function onMouseMove(event) {
            if (event.movementY < 0) {
                resolve(9);
            } else if (event.movementY > 0) {
                resolve(10);
            } else if (event.movementX < 0) {
                resolve(11);
            } else if (event.movementX > 0) {
                resolve(12);
            } else {
                return; // Ignore other movements
            }
            document.removeEventListener("keydown", onKeyDown);
            document.removeEventListener("mousedown", onMouseDown);
            document.removeEventListener("mousemove", onMouseMove);
        }

        document.addEventListener("keydown", onKeyDown);
        document.addEventListener("mousedown", onMouseDown);
        document.addEventListener("mousemove", onMouseMove);
>>>>>>>> gerador-funcional:src/jogo/biblioteca.js
    });
}

/* -------------------------------------------------- */
/* HELPER FUNCTIONS: não precisam existir na linguagem dos alunos */
/* -------------------------------------------------- */

function redesenharTodosComExcecao(idExcecao) {
    for (let i = 0; i < listaDeObjetos.length; i++) {
        if (i !== idExcecao) {
            const obj = listaDeObjetos[i];
            if (obj.tipo === "imagem") {
                desenharImagem(obj.x, obj.y, obj.url);
            } else {
                desenharFigura(obj.tipo, obj.cor, obj.x, obj.y, obj.tamanho);
            }
        }
    }
}

function redesenharTodos() {
    for (let i = 0; i < listaDeObjetos.length; i++) {
        const obj = listaDeObjetos[i];
        if (obj.tipo === "imagem") {
            desenharImagem(obj.x, obj.y, obj.url);
        } else {
            desenharFigura(obj.tipo, obj.cor, obj.x, obj.y, obj.tamanho);
        }
    }
}

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function draw() {
    if (canvas.getContext) {
        const ctx = canvas.getContext("2d");
    }
}
window.addEventListener("load", draw);

window.addEventListener("keydown", event => {
    if (event.key === "ArrowLeft") {
        ultimaTecla = 3;
        console.log("Tecla pressionada: ArrowLeft (3)");
    } else if (event.key === "ArrowRight") {
        ultimaTecla = 4;
        console.log("Tecla pressionada: ArrowRight (4)");
    } else if (event.key === "ArrowUp") {
        ultimaTecla = 1;
        console.log("Tecla pressionada: ArrowUp (1)");
    } else if (event.key === "ArrowDown") {
        ultimaTecla = 2;
        console.log("Tecla pressionada: ArrowDown (2)");
    } else if (event.key === "Enter") {
        ultimaTecla = 6;
        console.log("Tecla pressionada: Enter (6)");
    } else if (event.key === " ") {
        ultimaTecla = 5;
        console.log("Tecla pressionada: Space (5)");
    }
});

window.addEventListener("mousedown", event => {
    if (event.button === 0) {
        ultimaTecla = 7;
        console.log("Mouse button pressed: Left (7)");
    } else if (event.button === 2) {
        ultimaTecla = 8;
        console.log("Mouse button pressed: Right (8)");
    }
});

document.addEventListener("mousemove", debounce(event => {
    const { movementX, movementY } = event;
    if (movementX > 0 && Math.abs(movementX) > Math.abs(movementY)) {
        ultimaTecla = 12;
        console.log("Mouse moved: Right (12)");
    } else if (movementX < 0 && Math.abs(movementX) > Math.abs(movementY)) {
        ultimaTecla = 11;
        console.log("Mouse moved: Left (11)");
    } else if (movementY > 0 && Math.abs(movementY) > Math.abs(movementX)) {
        ultimaTecla = 10;
        console.log("Mouse moved: Down (10)");
    } else if (movementY < 0 && Math.abs(movementY) > Math.abs(movementX)) {
        ultimaTecla = 9;
        console.log("Mouse moved: Up (9)");
    }
}, 50));