from AnalisadorLexico import AnalisadorLexico
from AnalisadorSemantico import AnalisadorSemantico
from ClassesAuxiliares import NoTabela, SemanticException, NoFolha, NoInterno

codigo_fonte ='''programa
"Programa com declaração duplicada de variáveis"
var
numero x, y, z;
texto a;
binario y, n;
{
x : 10;
y : criar_figura("quadrado", "#00FF00", 100, 50, 20);
se (x = y) {
tocar("musica.mp3");
} senao {
mostrar("Não faz nada");
}
}
'''
analise_lexica=AnalisadorLexico(codigo_fonte)
tokens=analise_lexica.getTokens()
print(tokens)
analise_semantica=AnalisadorSemantico(tokens)
print(analise_semantica.analisa())