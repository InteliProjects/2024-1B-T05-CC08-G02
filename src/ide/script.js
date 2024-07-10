document.addEventListener('DOMContentLoaded', function () {
    const $myCodeMirror = CodeMirror.fromTextArea(document.querySelector('#editor'), {
        lineNumbers: true,
        theme: 'monokai',
        mode: "javascript",
        outerHeight: 100
    });

    document.getElementById('compileBtn').addEventListener('click', function () {
        const code = $myCodeMirror.getValue();
        fetch('http://127.0.0.1:5000/run-python-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Erro na solicitação: ' + response.statusText);
            }
            return response.json();
        }).then(data => {
            if (data.error) {
                alert("Erro: " + data.error);
            } else {
                alert(data.output);
            }
        }).catch(error => {
            console.error('Erro na requisição:', error);
        });
    });

    document.getElementById('gerarBtn').addEventListener('click', function () {
        const code = $myCodeMirror.getValue();
        fetch('http://127.0.0.1:5000/gerar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Erro na solicitação: ' + response.statusText);
            }
            return response.json();
        }).then(data => {
            if (data.error) {
                alert("Erro: " + data.error);
            } else {
                alert(data.output);
            }
        }).catch(error => {
            console.error('Erro na requisição:', error);
        });
    });

    $('#saveBtn').click(function () {
        var terapeuta = $('#terapeutaInput').val();
        var paciente = $('#pacienteInput').val();
        var projeto = $('#projetoInput').val();
        var codigoFonte = $myCodeMirror.getValue();

        $.ajax({
            url: 'http://127.0.0.1:5000/save-data',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                terapeuta: terapeuta,
                paciente: paciente,
                projeto: projeto,
                codigoFonte: codigoFonte
            }),
            success: function (response) {
                if (response.status === 'success') {
                    alert('Dados salvos com sucesso!');
                    $('#terapeutaInput').val('');
                    $('#pacienteInput').val('');
                    $('#projetoInput').val('');
                    $myCodeMirror.setValue('');
                } else {
                    alert('Erro ao salvar dados: ' + response.message);
                }
            },
            error: function (error) {
                console.error('Erro na requisição:', error);
            }
        });
    });

    $('#loadBtn').click(function () {
        $.ajax({
            url: 'http://127.0.0.1:5000/get-data',
            method: 'GET',
            success: function (response) {
                if (response.status === 'success') {
                    const rowsContainer = $('#rowsContainer');
                    rowsContainer.empty(); // Clear any existing rows

                    response.data.forEach(row => {
                        const rowElement = $(`
                            <div class="row">
                                <span>${row.id}</span>
                                <span>${row.terapeuta}</span>
                                <span>${row.paciente}</span>
                                <span>${row.projeto}</span>
                                <button class="loadRowBtn" data-id="${row.id}">Carregar</button>
                            </div>
                        `);
                        rowsContainer.append(rowElement);
                    });

                    $('.loadRowBtn').click(function () {
                        const rowId = $(this).data('id');
                        const rowData = response.data.find(row => row.id === rowId);

                        $('#terapeutaInput').val(rowData.terapeuta);
                        $('#pacienteInput').val(rowData.paciente);
                        $('#projetoInput').val(rowData.projeto);
                        $myCodeMirror.setValue(rowData.codigoFonte);

                        $('#myModal').hide(); // Close the modal
                    });

                    $('#myModal').show(); // Show the modal
                } else {
                    alert('Erro ao carregar dados: ' + response.message);
                }
            },
            error: function (error) {
                console.error('Erro na requisição:', error);
            }
        });
    });

    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Adiciona o tutorial do Intro.js
    document.getElementById('startTutorial').addEventListener('click', function () {
        introJs().setOptions({
            steps: [
                {
                    intro: "Bem-vindo ao tutorial!"
                },
                {
                    element: document.querySelector('.column1'),
                    intro: "Esta é a seção de entrada. Aqui você pode inserir os detalhes do terapeuta, paciente e projeto.",
                    position: 'right'
                },
                {
                    element: document.getElementById('compileBtn'),
                    intro: "Este é o botão de compilar. Clique aqui para compilar seu código.",
                    position: 'right'
                },
                {
                    element: document.getElementById('loadBtn'),
                    intro: "Este é o botão de carregar. Clique aqui para carregar um projeto salvo.",
                    position: 'right'
                },
                {
                    element: document.querySelector('.column2'),
                    intro: "Este é o editor de código. Escreva seu código aqui.",
                    position: 'top'
                },
                {
                    element: document.getElementById('myModal'),
                    intro: "Esta é a janela modal onde você pode selecionar registros.",
                    position: 'top'
                },
                {
                    element: document.querySelector('.column3'),
                    intro: "Esta é a seção de imagens. Você pode importar imagens aqui.",
                    position: 'left'
                },
                {
                    element: document.getElementById('importBtn'),
                    intro: "Clique aqui para importar imagens.",
                    position: 'left'
                }
            ]
        }).start();
    });

    // Abrir o modal do glossário
    document.getElementById('glossarioBtn').addEventListener('click', function () {
        document.getElementById('glossarioModal').style.display = 'block';
    });

    // Fechar o modal do glossário
    var glossarioModal = document.getElementById("glossarioModal");
    var glossarioSpan = document.querySelector("#glossarioModal .close");

    glossarioSpan.onclick = function () {
        glossarioModal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == glossarioModal) {
            glossarioModal.style.display = "none";
        }
    }
});
