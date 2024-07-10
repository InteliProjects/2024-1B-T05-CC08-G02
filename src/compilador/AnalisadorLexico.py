import re
from ClassesAuxiliares import Token, LexicalException  # Importa a classe Token e a exceção LexicalException

class AnalisadorLexico:
    def __init__(self, codigoFonte):
        self.codigo = codigoFonte
        self.removeComentarios()  # Remove os comentários do código

    def removeComentarios(self):
        codigo_sem_comentarios = ""  # Inicializa uma string para armazenar o código sem comentários
        dentro_comentario_multilinha = False  # Define uma flag para controlar se está dentro de um comentário de múltiplas linhas

        i = 0
        while i < len(self.codigo):
            if self.codigo[i] == '\n':  # Se encontrar uma quebra de linha
                codigo_sem_comentarios += '\n'  # Adiciona a quebra de linha à string sem comentários
                i += 1
            elif not dentro_comentario_multilinha and self.codigo[i]== "#" and self.codigo[i-1]!="\"":
                # Se não estiver dentro de um comentário de múltiplas linhas e encontrar o início de um comentário de linha
                while i < len(self.codigo) and self.codigo[i] != '\n':
                    i += 1  # Avança até o final da linha
            elif not dentro_comentario_multilinha and i + 1 < len(self.codigo) and self.codigo[i:i + 2] == "/#":
                # Se não estiver dentro de um comentário de múltiplas linhas e encontrar o início de um comentário de múltiplas linhas
                dentro_comentario_multilinha = True  # Ativa a flag indicando que está dentro de um comentário de múltiplas linhas
                i += 2
            elif dentro_comentario_multilinha and i + 1 < len(self.codigo) and self.codigo[i:i + 2] == "#/":
                # Se estiver dentro de um comentário de múltiplas linhas e encontrar o fim do comentário
                dentro_comentario_multilinha = False  # Desativa a flag indicando que não está mais dentro de um comentário de múltiplas linhas
                i += 2
            elif not dentro_comentario_multilinha:
                # Se não estiver dentro de um comentário de múltiplas linhas
                codigo_sem_comentarios += self.codigo[i]  # Adiciona o caractere à string sem comentários
                i += 1
            else:
                i += 1

        self.codigo = codigo_sem_comentarios  # Atualiza o código removendo os comentários

    def reserved_symbols(self, symbol, line):
        # Dicionário que mapeia os símbolos reservados para seus tipos correspondentes
        type_symbols = {
            'programa': 'PROGRAMA', 'var': 'VAR', 'binario': 'TYPE', 'numero': 'TYPE', 'texto': 'TYPE',
            'se': 'SE', 'senao': 'SENAO', 'enquanto': 'ENQUANTO', 'repita': 'REPITA', 'v': 'BOOL',
            'f': 'BOOL', ':': 'ASSIGN', ',': 'COMMA', ';': 'SEMICOLON', '"':'DQUOTE', '(': 'LPAR',
            ')': 'RPAR', '{': 'LBLOCK', '}': 'RBLOCK', 'ler_numero': 'FUNCIN', 'ler_binario': 'FUNCIN',
            'ler': 'FUNCIN', 'consultar': 'FUNCIN', 'criar_figura': 'FUNCIN', 'criar_imagem': 'FUNCIN',
            'colidiu': 'FUNCIN', 'aleatorio': 'FUNCIN', 'mostrar': 'FUNCOUT', 'limpar': 'FUNCOUT',
            'inicializar_com_cor': 'FUNCOUT', 'inicializar_com_imagem': 'FUNCOUT',
            'redefinir_figura': 'FUNCOUT', 'redefinir_imagem': 'FUNCOUT', 'mover': 'FUNCOUT',
            'destacar': 'FUNCOUT', 'reverter_destaque': 'FUNCOUT', 'tocar': 'FUNCOUT', 'esperar': 'FUNCOUT',
            '=': 'OPREL', '!=': 'OPREL', '<': 'OPREL', '<=': 'OPREL', '>': 'OPREL', '>=': 'OPREL', '+': 'OPSUM',
            '-': 'OPSUM', 'ou': 'OPSUM', '*': 'OPMUL', '/': 'OPMUL', '%': 'OPMUL', 'e': 'OPMUL', '^': 'OPPOW','nao':'NAO', 'EOF': 'EOF'
        }
        try:
            return Token(type_symbols[symbol], symbol, line)  # Retorna um token com o tipo correspondente ao símbolo, o próprio símbolo e a linha
        except:
            raise LexicalException( "Símbolo inválido na linha "+str(line)+": "+symbol)# Lança uma exceção se o caractere não for reconhecido
    def getTokens(self):
        i = 0
        actualLine = 1
        tokens = []  # Inicializa uma lista para armazenar os tokens
        isString = False  # Define uma flag para controlar se está dentro de uma string
        actualWord = ""  # Inicializa uma string para armazenar a palavra atual
        actualNumber = ""  # Inicializa uma string para armazenar o número atual
        insideString=0
        possibilities_reserved = ["nao","programa","var","binario","numero","texto","se","senao","enquanto","repita","v","f","ler_numero","ler_binario","ler","consultar","criar_figura","criar_imagem","colidiu","aleatorio","mostrar","limpar",'inicializar_com_cor', 'inicializar_com_imagem','redefinir_figura', 'redefinir_imagem', 'mover','destacar', 'reverter_destaque', 'tocar', 'esperar',"e"]

        while i < len(self.codigo):
            if re.search('["{},;=()<>/|!+-:%*#^\n\s\w\t"]+', self.codigo[i]) is not None:
                # Se o caractere atual corresponder a algum padrão de símbolo ou palavra-chave
                if isString:
                    actualWord += self.codigo[i]  # Adiciona o caractere à palavra atual se estiver dentro de uma string
                else:
                    if re.search("[_a-zA-Z#\"][_a-zA-Z0-9#\"]*", self.codigo[i]) != None or self.codigo[i]=="#":
                        # Se o caractere atual for parte de uma palavra
                        pos = i
                        while re.search("[_a-zA-Z#\"][_a-zA-Z0-9#\"]*", self.codigo[pos]) != None or self.codigo[pos].isnumeric()or self.codigo[i]=="#":
                            # Enquanto a próxima parte da palavra for válida
                            if(self.codigo[pos]=="\"" and self.codigo[pos-1]!="\\"):
                                tokens.append(Token("DQUOTE","\"", actualLine))
                                insideString+=1
                                pos+=1
                                while pos < len(self.codigo) and self.codigo[pos] != "\"":
                                    if pos == len(self.codigo):
                                        break
                                    if self.codigo[pos] == "\\" and pos + 1 < len(self.codigo) and self.codigo[pos+1]=="\"":
                                        actualWord+="\\"+"\""
                                        pos+=2
                                    actualWord+=self.codigo[pos]
                                    pos+=1
                                    if pos>len(self.codigo):
                                        break
                                break
                            actualWord += self.codigo[pos]  # Adiciona o caractere à palavra atual
                            pos += 1
                            if pos >= len(self.codigo):
                                break
                        if len(actualWord) > 0:
                            if actualWord in possibilities_reserved:
                                tokens.append(self.reserved_symbols(actualWord, actualLine))  # Adiciona um token de palavra-chave se a palavra estiver entre as possibilidades reservadas
                            else:
                                if(insideString!=0):
                                    tokens.append(Token("STR",actualWord, actualLine))
                                    tokens.append(Token("DQUOTE","\"", actualLine))
                                    insideString=0
                                    pos+=1
                                else:
                                    tokens.append(Token("ID",actualWord, actualLine))  # Adiciona um token de identificador caso contrário
                            actualWord = ""  # Reinicia a palavra atual
                            i = pos - 1  # Atualiza o índice para a próxima posição
                    elif self.codigo[i] in "!=<>" and i + 1 < len(self.codigo):
                        # Se o caractere atual for "=", "<" ou ">" e houver um próximo caractere
                        symbol = self.codigo[i] + self.codigo[i+1]  # Concatena o caractere atual com o próximo
                        if symbol in ("==", "<=", ">=","!="):
                            tokens.append(self.reserved_symbols(symbol, actualLine))  # Adiciona um token correspondente ao símbolo de dois caracteres
                            i += 1  # Avança o índice para o próximo caractere
                        else:
                            tokens.append(self.reserved_symbols(self.codigo[i], actualLine))  # Adiciona um token correspondente ao símbolo de um caractere

                    elif re.search("[0-9]+", self.codigo[i]) != None:
                        # Se o caractere atual for um dígito
                        pos = i
                        while re.search("[0-9]+", self.codigo[pos]) != None:
                            # Enquanto a próxima parte for um dígito
                            actualNumber += self.codigo[pos]  # Adiciona o dígito ao número atual
                            pos += 1
                            if pos == len(self.codigo):
                                break
                        if len(actualNumber) > 0:
                            tokens.append(Token("INT", int(actualNumber), actualLine))  # Adiciona um token de número inteiro
                            actualNumber = ""  # Reinicia o número atual
                            i = pos - 1  # Atualiza o índice para a próxima posição
                    elif self.codigo[i] not in " \n\t\r":
                        if (self.codigo[i] == "\""):
                            isString = True  # Ativa a flag indicando que está dentro de uma string
                        tokens.append(self.reserved_symbols(self.codigo[i], actualLine))  # Adiciona um token do símbolo atual
            else:
                raise LexicalException( "Símbolo inválido na linha "+str(actualLine)+": "+self.codigo[i])
                
            if self.codigo[i] == "\n":
                actualLine += 1  # Atualiza o número da linha se encontrar uma quebra de linha
            i += 1  # Avança para o próximo caractere
        tokens.append(Token("EOF", "EOF", actualLine))  # Adiciona um token de fim de arquivo
        return tokens  # Retorna a lista de tokens