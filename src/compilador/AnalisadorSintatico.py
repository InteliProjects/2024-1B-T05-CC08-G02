import re
from ClassesAuxiliares import LexicalException, SyntaxException, Token, NoInterno, NoFolha

class AnalisadorSintatico:
    def __init__(self, listaTokens):
        self.tokens = listaTokens
        self.tokenCorrente = None
        self.posicao = -1
        self.proximoToken()

    def proximoToken(self):
        if self.posicao < len(self.tokens) - 2:
            self.posicao += 1
            self.tokenCorrente = self.tokens[self.posicao]
    def lancarErro(self, tipoEsperado=None):
        """
		Método que lança uma exceção do tipo SyntaxException.
		Ele será chamado pelo método comparar() quando o token esperado for diferente do token corrente.

		OBS: Não modifique as mensagens de erro!
		OBS: Não é necessário modificar este método.
		"""
        if tipoEsperado:
            raise SyntaxException(f"Token inesperado: \"{self.tokenCorrente.tipo}\" ({self.tokenCorrente.valor}), tipo esperado: \"{tipoEsperado}\", na linha {self.tokenCorrente.linha}")
        else:
            raise SyntaxException(f"Token inesperado: \"{self.tokenCorrente.tipo}\" ({self.tokenCorrente.valor}) na linha {self.tokenCorrente.linha}")


    def comparar(self, tipoEsperado):
        tokenRetorno = self.tokenCorrente
        if self.tokenCorrente.tipo.upper() == tipoEsperado.upper():
            self.proximoToken()
        else:
            self.lancarErro(tipoEsperado)
        return tokenRetorno


    def analisar(self):
        return self.program()

    def program(self):
        self.comparar("PROGRAMA")  # Verifica se o token atual é "PROGRAMA"
        no_str = self.str()  # Processa a string
        self.comparar("VAR")  # Verifica se o próximo token é "VAR"
        no_var_declaration_list = self.varDeclarationList()  # Processa a lista de declarações de variáveis
        no_block = self.block()  # Processa o bloco de código
        self.comparar("EOF")  # Verifica se o próximo token é "EOF"
        return NoInterno(op="alg", id=no_str, declarations=no_var_declaration_list, block=no_block)


    def str(self):
        self.comparar("DQUOTE")  # Compara e avança para o próximo token do tipo "DQUOTE"
        token_str = self.comparar("STR")  # Compara e avança para o próximo token do tipo "STR"
        folha_str = NoFolha(op="id", valor=token_str.valor, linha=token_str.linha)
        self.comparar("DQUOTE")  # Compara e avança para o próximo token do tipo "DQUOTE"
        return folha_str

    def varDeclarationList(self):
        no = None
        if self.tokenCorrente.tipo == "TYPE":
            no_var_declaration = self.varDeclaration()  # Chama o método varDeclaration() para tratar a declaração de variável
            no_var_declaration_list = self.varDeclarationList()  # Chama recursivamente varDeclarationList() para tratar o restante da lista
            no = NoInterno(op="varDeclarationList", varDeclaration=no_var_declaration, prox=no_var_declaration_list)
        return no

    def varDeclaration(self):
        token_type = self.comparar("TYPE")  # Compara e avança para o próximo token do tipo "TYPE"
        no_identifier_list = self.identifierList()  # Chama o método identifierList() para tratar a lista de identificadores
        self.comparar("SEMICOLON")  # Compara e avança para o próximo token do tipo "SEMICOLON"
        return NoInterno(op="varDeclaration", type=NoFolha(op="type", valor=token_type.valor, linha=token_type.linha), identifierList=no_identifier_list)

    def identifierList(self):
        no = None
        if self.tokenCorrente.tipo == "ID":
            token_id = self.comparar("ID")  # Compara e avança para o próximo token do tipo "ID"
            folha_id = NoFolha(op="id", valor=token_id.valor, linha=token_id.linha)
            if self.tokenCorrente.tipo == "COMMA":
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                no_identifier_list = self.identifierList()  # Chama recursivamente identifierList() para tratar o restante da lista
                no = NoInterno(op="identifierList", id=folha_id, prox=no_identifier_list)
            else:
                no = NoInterno(op="identifierList", id=folha_id, prox=None)
        return no

    def block(self):
        self.comparar("LBLOCK")  # Compara e avança para o próximo token do tipo "LBLOCK"
        no_statement_list = self.statementList()  # Chama o método statementList() para tratar a lista de comandos
        self.comparar("RBLOCK")  # Compara e avança para o próximo token do tipo "RBLOCK"
        return NoInterno(op="block", statementList=no_statement_list)

    def statementList(self):
        no = None
        if self.tokenCorrente.tipo != "RBLOCK":
            no_statement = self.statement()  # Chama o método statement() para tratar um comando
            no_statement_list = self.statementList()  # Chama recursivamente statementList() para tratar o restante da lista
            no = NoInterno(op="statementList", statement=no_statement, prox=no_statement_list)
        return no

    def statement(self):
        if self.tokenCorrente.tipo == "SE":
            return self.ifStatement()  # Chama o método ifStatement() para tratar uma estrutura condicional
        elif self.tokenCorrente.tipo == "ENQUANTO":
            return self.whileStatement()  # Chama o método whileStatement() para tratar um loop while
        elif self.tokenCorrente.tipo == "REPITA":
            return self.repeatStatement()  # Chama o método repeatStatement() para tratar um loop repeat
        elif self.tokenCorrente.tipo == "FUNCOUT":
            return self.commandStatement()  # Chama o método commandStatement() para tratar um comando de função
        elif self.tokenCorrente.tipo == "ID":
            return self.assignStatement()  # Chama o método assignStatement() para tratar uma atribuição

    def assignStatement(self):
        token_id = self.comparar("ID")  # Compara e avança para o próximo token do tipo "ID"
        folha_id = NoFolha(op="id", valor=token_id.valor, linha=token_id.linha)
        self.comparar("ASSIGN")  # Compara e avança para o próximo token do tipo "ASSIGN"
        if self.tokenCorrente.tipo == "FUNCIN":
            no_expr = self.inputStatement()  # Chama o método inputStatement() para tratar a entrada de dados
        elif self.tokenCorrente.tipo in ["DQUOTE", "STR"]:
            no_expr = self.str()  # Chama o método str() para tratar uma string
        else:
            no_expr = self.expression()  # Chama o método expression() para tratar uma expressão matemática
        self.comparar("SEMICOLON")  # Compara e avança para o próximo token do tipo "SEMICOLON"
        return NoInterno(op="assignStatement", id=folha_id, expression=no_expr)

    def inputStatement(self):
        token_funcin = self.comparar("FUNCIN")  # Compara e avança para o próximo token do tipo "FUNCIN"
        self.comparar("LPAR")  # Compara e avança para o próximo token do tipo "LPAR"
        if token_funcin.valor in ["ler_numero", "ler_binario"]:
            no_str = self.str()  # Chama o método str() para tratar uma string
            self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
            return NoInterno(op="inputStatement", func=token_funcin.valor, string=no_str)
        elif token_funcin.valor in ["ler", "consultar"]:
            self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
            return NoInterno(op="inputStatement", func=token_funcin.valor)
        elif token_funcin.valor in ["criar_figura", "criar_imagem", "colidiu", "aleatorio"]:
            args = []
            if token_funcin.valor == "criar_figura":
                args.append(self.str())  # Chama o método str() para tratar uma string
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                args.append(self.str())  # Chama o método str() para tratar uma string
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
            elif token_funcin.valor == "criar_imagem":
                args.append(self.str())  # Chama o método str() para tratar uma string
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
            elif token_funcin.valor in ["colidiu", "aleatorio"]:
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
            self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
            return NoInterno(op="inputStatement", func=token_funcin.valor, args=args)

    def ifStatement(self):
        self.comparar("SE")  # Compara e avança para o próximo token do tipo "SE"
        self.comparar("LPAR")  # Compara e avança para o próximo token do tipo "LPAR"
        no_expr = self.logicalOrExpression()  # Chama o método logicalOrExpression() para tratar uma expressão lógica
        self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
        no_block = self.block()  # Chama o método block() para tratar o bloco de comandos
        no_else_block = None
        if self.tokenCorrente.tipo == "SENAO":
            self.comparar("SENAO")  # Compara e avança para o próximo token do tipo "SENAO"
            no_else_block = self.block()  # Chama o método block() para tratar o bloco de comandos do "SENAO"
        return NoInterno(op="ifStatement", expression=no_expr, blockIf=no_block, blockElse=no_else_block)

    def whileStatement(self):
        self.comparar("ENQUANTO")  # Compara e avança para o próximo token do tipo "ENQUANTO"
        self.comparar("LPAR")  # Compara e avança para o próximo token do tipo "LPAR"
        no_expr = self.logicalOrExpression()  # Chama o método logicalOrExpression() para tratar uma expressão lógica
        self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
        no_block = self.block()  # Chama o método block() para tratar o bloco de comandos
        return NoInterno(op="whileStatement", expression=no_expr, block=no_block)

    def repeatStatement(self):
        self.comparar("REPITA")  # Compara e avança para o próximo token do tipo "REPITA"
        self.comparar("LPAR")  # Compara e avança para o próximo token do tipo "LPAR"
        no_expr = self.sumExpression1()  # Chama o método sumExpression1() para tratar uma expressão matemática
        self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
        no_block = self.block()  # Chama o método block() para tratar o bloco de comandos
        return NoInterno(op="repeatStatement", expression=no_expr, block=no_block)

    def commandStatement(self):
        token_funcout = self.comparar("FUNCOUT")  # Compara e avança para o próximo token do tipo "FUNCOUT"
        self.comparar("LPAR")  # Compara e avança para o próximo token do tipo "LPAR"
        args = []
        if token_funcout.valor == "mostrar":
            if self.tokenCorrente.tipo in ["DQUOTE", "STR"]:
                args.append(self.str())  # Chama o método str() para tratar uma string
            else:
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
        elif token_funcout.valor == "limpar":
            pass
        elif token_funcout.valor in ["inicializar_com_cor", "tocar"]:
            args.append(self.str())  # Chama o método str() para tratar uma string
        elif token_funcout.valor in ["inicializar_com_imagem", "destacar"]:
            args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
        elif token_funcout.valor in ["redefinir_figura", "redefinir_imagem", "mover"]:
            args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
            self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
            args.append(self.str())  # Chama o método str() para tratar uma string
            self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
            args.append(self.str())  # Chama o método str() para tratar uma string
            self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
            args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
            self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
            args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
            if token_funcout.valor == "redefinir_figura":
                self.comparar("COMMA")  # Compara e avança para o próximo token do tipo "COMMA"
                args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
        elif token_funcout.valor == "reverter_destaque":
            pass
        elif token_funcout.valor == "esperar":
            args.append(self.sumExpression1())  # Chama o método sumExpression1() para tratar uma expressão matemática
        self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
        self.comparar("SEMICOLON")  # Compara e avança para o próximo token do tipo "SEMICOLON"
        return NoInterno(op="commandStatement", func=token_funcout.valor, args=args)

    """
    def logicalOrExpression(self):
        no_left = self.logicalAndExpression()  # Chama o método logicalAndExpression() para tratar uma expressão lógica
        while self.tokenCorrente.tipo == "ID" and self.tokenCorrente.valor == "ou":
            token_op = self.comparar("ID")  # Compara e avança para o próximo token do tipo "ID"
            no_right = self.logicalAndExpression()  # Chama o método logicalAndExpression() para tratar uma expressão lógica
            no_left = NoInterno(op="logicalOrExpression", left=no_left, logical_op=token_op.valor, right=no_right)
        return no_left

    def logicalAndExpression(self):
        no_left = self.expression()  # Chama o método expression() para tratar uma expressão matemática
        while self.tokenCorrente.tipo == "ID" and self.tokenCorrente.valor == "e":
            token_op = self.comparar("ID")  # Compara e avança para o próximo token do tipo "ID"
            no_right = self.expression()  # Chama o método expression() para tratar uma expressão matemática
            no_left = NoInterno(op="logicalAndExpression", left=no_left, logical_op=token_op.valor, right=no_right)
        return no_left
    """

    def expression(self):
        no_left = self.sumExpression1()  # Chama o método sumExpression1() para tratar uma expressão matemática
        no_right=None
        token_oprel=None
        if self.tokenCorrente.tipo == "OPREL":
            token_oprel = self.comparar("OPREL")  # Compara e avança para o próximo token do tipo "OPREL"
            no_right = self.sumExpression1()  # Chama o método sumExpression1() para tratar uma expressão matemática
        return NoInterno(op="expression", esq=no_left, oper=token_oprel.valor, dir=no_right)

    def sumExpression1(self):
        no_left = self.multTerm()  # Chama o método multTerm() para tratar um termo multiplicativo
        return self.sumExpression2(no_left)  # Chama o método sumExpression2() para tratar uma expressão matemáti

    def sumExpression2(self, esq):
        no = None
        if self.tokenCorrente.tipo == "OPSUM":
            token_opsum = self.comparar("OPSUM")  # Compara e avança para o próximo token do tipo "OPSUM"
            no_right = self.multTerm()  # Chama o método multTerm() para tratar um termo multiplicativo
            no = NoInterno(op="sumExpression", oper=token_opsum.valor, esq=esq, dir=no_right)  # Chama o método sumExpression2() recursivamente para tratar uma expressão matemática
            return self.sumExpression2(no)
        return no

    def multTerm(self):
        no_left = self.powerTerm()  # Chama o método powerTerm() para tratar um termo de potência
        return self.multTerm2(no_left)  # Chama o método multTerm2() para tratar um termo multiplicativo
        
    def multTerm2(self, esq=None):
        no = None
        if self.tokenCorrente.tipo == "OPMUL":
            token_opmul = self.comparar("OPMUL")  # Compara e avança para o próximo token do tipo "OPMUL"
            no_right = self.powerTerm()  # Chama o método powerTerm() para tratar um termo de potência
            no = NoInterno(op="multiplicativeTerm", oper=token_opmul.valor, esq=esq, dir=no_right)  # Chama o método multTerm2() recursivamente para tratar um termo multiplicativo
            return self.multTerm2(no)
        return no

    def powerTerm(self):
        no_left = self.factor()  # Chama o método factor() para tratar um fator
        no_right = None
        if self.tokenCorrente.tipo == "OPPOW":
            token_oppow = self.comparar("OPPOW")  # Compara e avança para o próximo token do tipo "OPPOW"
            no_right = self.powerTerm()  # Chama o método powerTerm() recursivamente para tratar um termo de potência
            return NoInterno(op="powerTerm", oper=token_oppow.valor, esq=no_left, dir=no_right)
        return no_left

    def factor(self):
        sinal = "+"
        if self.tokenCorrente.tipo == "OPSUM":
            token = self.comparar("OPSUM")  # Compara e avança para o próximo token do tipo "OPSUM"
            if token.valor == "-":
                sinal = "-"
        elif self.tokenCorrente.tipo == "NAO":
            token = self.comparar("NAO")  # Compara e avança para o próximo token do tipo "OPSUM"
            if token.valor == "nao":
                sinal = "NAO"        
        if self.tokenCorrente.tipo == "ID":
            token_id = self.comparar("ID")  # Compara e avança para o próximo token do tipo "ID"
            folha = NoFolha(op="id", valor=token_id.valor, linha=token_id.linha)  # Retorna um nó folha com o tipo "id"
            return NoInterno(op="factor", sinal=sinal, esq=None, dir=None, factor=folha)
        elif self.tokenCorrente.tipo == "INT":
            token_int = self.comparar("INT")  # Compara e avança para o próximo token do tipo "INT"
            folha = NoFolha(op="int", valor=token_int.valor, linha=token_int.linha)  # Retorna um nó folha com o tipo "num"
            return NoInterno(op="factor", sinal=sinal, esq=None, dir=None, factor=folha)
        elif self.tokenCorrente.tipo == "BOOL":
            token_bool = self.comparar("BOOL")  # Compara e avança para o próximo token do tipo "BOOL"
            folha = NoFolha(op="bool", valor=token_bool.valor, linha=token_bool.linha)  # Retorna um nó folha com o tipo "bool"
            return NoInterno(op="factor", sinal=sinal, esq=None, dir=None, factor=folha)
        elif self.tokenCorrente.tipo == "LPAR":
            self.comparar("LPAR")  # Compara e avança para o próximo token do tipo "LPAR"
            no_expr = self.expression()  # Chama o método logicalOrExpression() para tratar uma expressão lógica
            self.comparar("RPAR")  # Compara e avança para o próximo token do tipo "RPAR"
            return NoInterno(op="factor", sinal=sinal, esq=None, dir=None, expression=no_expr)  # Retorna a expressão lógica