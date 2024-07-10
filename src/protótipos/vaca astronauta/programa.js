async function main(){
    var numero, obj, tecla;
    mostrar("Aperte a seta para cima.")
    tecla = await ler();
    
    if (tecla == 1){
        obj = criar_imagem("vaca_astronauta.jpg", 720, 0);
        tocar("nave_abrindo.mp3");
        esperar(2);
        tocar("muu.mp3");
    }
}
main()
