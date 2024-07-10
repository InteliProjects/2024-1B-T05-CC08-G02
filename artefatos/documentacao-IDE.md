# Documentação do Sistema de IDE para Terapia Ocupacional

## Visão Geral

 Este sistema é uma IDE (Ambiente de Desenvolvimento Integrado) desenvolvida para auxiliar terapeutas ocupacionais na criação de programas lúdicos para crianças com necessidades especiais. A interface permite que os terapeutas insiram detalhes sobre seus pacientes e projetos, compilando e executando códigos diretamente na plataforma. O objetivo principal é proporcionar uma ferramenta prática e intuitiva que facilita a personalização de atividades terapêuticas.

 ## Objetivos

 - Facilitar a criação e execução de programas de terapia ocupacional personalizados.
- Permitir o armazenamento e recuperação de projetos salvos.
- Oferecer uma interface intuitiva e responsiva para os terapeutas.
- Incluir um tutorial interativo para novos usuários.

## Funcionalidades Principais

### Entrada de Dados
A interface principal possui uma seção de entrada de dados onde o terapeuta pode inserir informações essenciais para o projeto:

- Terapeuta: Campo para inserir o nome do terapeuta responsável.
- Paciente: Campo para inserir o nome do paciente.
- Projeto: Campo para inserir o nome do projeto.
- URL da Imagem: Campo para inserir um link para uma imagem associada ao projeto.
- Arquivo de Imagem: Opção para fazer upload de uma imagem diretamente.

## Editor de Código

O editor de código permite que o terapeuta escreva e edite programas diretamente na plataforma. Ele suporta a linguagem de programação específica do sistema e oferece:

- Sintaxe destacada: Facilita a leitura e escrita de código.
- Linhas numeradas: Ajuda na navegação e depuração do código.
- Tema customizável: Apresenta um esquema de cores adequado para o uso prolongado.
- Placeholder: O editor possui um placeholder "Escreva aqui o código do jogo" para orientar os usuários.

## Botões de Ação

Abaixo dos campos de entrada de dados, estão disponíveis três botões de ação principais:

- Salvar: Salva os dados do projeto atual no banco de dados.
- Executar: Compila e executa o código escrito no editor.
- Abrir: Abre um modal para selecionar e carregar um projeto salvo anteriormente.

## Modal de Seleção

Quando o botão "Abrir" é clicado, um modal aparece permitindo que o terapeuta selecione um projeto salvo para carregar no editor. Este modal exibe uma lista de projetos com informações básicas como ID, nome do terapeuta, nome do paciente e nome do projeto.

## Tutorial Interativo
O sistema inclui um tutorial interativo implementado usando Intro.js, que guia novos usuários através das principais funcionalidades da plataforma:

- Introdução à interface: Explica os diferentes componentes da interface.
- Uso do editor de código: Demonstra como escrever e editar código.
- Salvamento e abertura de projetos: Orienta sobre como salvar e abrir projetos.

## Organização do Código

### HTML
A estrutura do HTML é dividida em três colunas principais:

- Column1: Contém os campos de entrada e botões de ação.
- Column2: Contém o editor de código e o título "Escreva a brincadeira".
- Column3: Reservado para a importação e visualização de imagens.

### CSS
O CSS define o layout responsivo e estiliza os componentes da interface:

- Flexbox: Usado para organizar as colunas e garantir a responsividade.
- Estilização dos botões: Inclui transições suaves e feedback visual ao passar o mouse.
- Tema do editor: Definido para garantir boa legibilidade e conforto visual.

### JavaScript
O JavaScript gerencia as interações dinâmicas da página:

- Eventos de clique: Gerencia as ações dos botões "Salvar", "Executar" e "Abrir".
- AJAX: Utilizado para enviar e receber dados do backend sem recarregar a página.
- Tutorial: Implementado usando o Intro.js para guiar novos usuários pela interface.

### Backend (server.py)
O backend foi desenvolvido usando Flask, que é um framework leve para a criação de APIs em Python. Ele é responsável por gerenciar a comunicação entre o frontend e o banco de dados, bem como por compilar e executar o código escrito pelos terapeutas.

#### Principais Funções

- init_db: Inicializa o banco de dados SQLite e cria a tabela jogos2 se ela não existir.
- run_python_code: Recebe o código via POST, o compila e retorna os tokens ou erros.
- save_data: Salva os dados do projeto (terapeuta, paciente, projeto, código) no banco de dados.
- get_data: Recupera os dados salvos dos projetos para exibição no frontend.
- add_image: Atualiza a URL ou BLOB da imagem no banco de dados.
- get_image: Recupera a URL ou BLOB da imagem do banco de dados para exibição.
