// programa "leao"
async function main(){
    var numero, obj, tecla;
    mostrar("Aperte a seta para cima.")
    tecla = await ler();

    if (tecla == 1){
        obj = criar_imagem("leao.png", 480, 270);
        tocar("leao.mp3");
    }
}
main()
