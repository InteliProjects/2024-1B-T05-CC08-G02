<table>
<tr>
<td>
<a href= "https://www.fm.usp.br/fofito/portal/"> <img src="fmusp-logo.svg" alt="FMUSP" border="0" width="90%"></a>
</td>
<td><a href= "https://www.inteli.edu.br/"><img src="inteli-logo.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0" width="35%"></a>
</td>
</tr>
</table>

# Introdução
Este é um dos repositórios do projeto de alunos do Inteli em parceria com o Departamento de Fisioterapia, Fonoaudiologia e Terapia Ocupacional (FOFITO) da Faculdade de Medicina da Universidade de São Paulo (FMUSP). Este projeto foi desenvolvido no 1º semestre de 2024 por alunos do Módulo 8 do curso de Ciência da Computação.

# Projeto: *Tapete sensorial como recurso lúdico para assistência a crianças com Transtorno do Espectro Autista.*

# Grupo: *Pimpolhos*

# Integrantes:
* [Arthur Nisa](mailto:Arthur.Souza@sou.inteli.edu.br)
* [Bruno Wasserstein](mailto:Bruno.Wasserstein@sou.inteli.edu.br)
* [Raab Iane](mailto:Raab.Silva@sou.inteli.edu.br)
* [Thomaz Klifson](mailto:Thomaz.Barboza@sou.inteli.edu.br)
* [Vinicius Kumagai](mailto:Vinicius.Kumagai@sou.inteli.edu.br)

# Descrição
O projeto desenvolve um recurso inovador e de baixo custo para auxiliar no atendimento de crianças com Transtorno do Espectro Autista (TEA) em Terapia Ocupacional. Através da interação física e digital, o tapete oferece estimulação sensorial e motora personalizada, além de proporcionar um ambiente lúdico e acolhedor na sala de espera, reduzindo a ansiedade antes das sessões. A integração com uma IDE permite aos terapeutas personalizarem os estímulos de acordo com as necessidades individuais de cada criança, tornando o tratamento mais eficaz e adaptado.

# Configuração para desenvolvimento

### Glossário

* **IDE:** Ambiente de Desenvolvimento Integrado (em inglês, Integrated Development Environment). Software que auxilia na programação, fornecendo recursos como editor de código, compilador, depurador e interface gráfica.
* **Backend:** Parte do software que fica em execução no servidor e processa as requisições dos usuários.
* **Analisador Léxico:** Ferramenta que divide o código-fonte em tokens, que são unidades básicas da linguagem de programação.
* **Analisador Sintático:** Ferramenta que verifica se a estrutura do código-fonte está de acordo com as regras da linguagem de programação.
* **Analisador Semântico:** Verifica se o código faz sentido na linguagem de programação, como tipos corretos e uso adequado de variáveis.
* **Gerador de Código Intermediário:** Transforma o código em uma forma mais fácil para o computador entender, como uma linguagem de montagem simplificada.

## Instruções para executar a IDE

1. Vá até a pasta `\src\ide`.
2. Execute o comando `npx http-server` no terminal.
3. No navegador, acesse qualquer um dos URLs exibidos no terminal.

## Instruções para executar o Backend

Para rodar o backend:

1. Vá até a pasta `\src\backend`.
2. No terminal, digite os seguintes comandos, pressionando Enter após cada um:
```
pip install flask
pip install flask-cors
pip install requests
```
3. Digite o comando `python server.py` e pressione Enter.

## Instruções para executar um Jogo.

1. Vá até a pasta `\src\jogo`.
2. Execute o comando `python -m http.server 8000` no terminal.
3. No navegador, acesse qualquer um dos URLs exibidos no terminal.

**Nota:** Utilize com frequência o comando **ctrl+shift+r** para atualizar a página, principalmente após gerar o código em JavaScript.

## Resultado final

Depois de criar o seu código na IDE, clique no botão "Verificar" para validar o seu código e garantir que não há erros. Em seguida, clique em "Gerar". Esse processo pode levar alguns segundos enquanto o sistema cria a versão final do seu código. Após a geração, clique no link "Página do jogo" para acessar e visualizar o jogo gerado.

Com isso, você deve estar rodando a IDE na porta 8080, o backend na porta 5000 e o jogo na porta 8000.

# Tags

* SPRINT 1:
  * Entendimento da Experiência do Usuário
  * Entendimento de negócios
  * Definição da arquitetura do sistema
* SPRINT 2:
  * IDE - 1ª Versão
  * Artigo - versão inicial
  * Analisador Léxico
* SPRINT 3:
  * Analisador Sintático
  * IDE - 2a versão
  * Artigo - versão 2
* SPRINT 4:
  * Analisador semântico e Geração de código
  * IDE - 3a versão
  * Artigo - versão 3
* SPRINT 5:
  * Analisadores léxico, sintático e semântico (versões finais)
  * Refinamento IDE
  * Artigo - versão final
  * Organização do Github

# Licença

<table>
  <tr><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"></tr>
</table>

<table>
  <tr><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></tr>
</table>

[Application 4.0 International](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)

