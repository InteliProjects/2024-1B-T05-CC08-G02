from ClassesAuxiliares import NoInterno, NoFolha

class GeradorCodigo:
    
    def __init__(self, arvore):
        self.arvore = arvore
        self.saida = "" #Saida do código (o código gerado)
        self.numTabs = -1 #Variável que conta o número de tabs
        self.simboloTab = "    " #Variável que representa a identação do Tab
        self.varTemp = 0  # Guardar o número de variáveis temporárias.
        self.binario = 0  # Variável do tipo binário começa vazia
        self.num = 0  # Variável do tipo numero começa vazia
        self.string = ""  # Variável do tipo string começa vazia

    def gerarJs(self):
        ##Recebe descrição do programa em variável temporária, adicionando no self.saida, a ser implementado
        self.saida += "//Código em JS\n"
        self.saida += f" Inicialização de variáveis"
        self.visitarVarDeclarationList(self.arvore.get("varDeclaration"))
        self.saida += f"# Início do código\n"
        self.visitarBlock(self.arvore.get("block"))
        return self.saida

    def visitarVarDeclarationList(self, no):
        #Começa chamando as variaváveis declaradas e percorre a lista encadeada
        if no:
            self.visitarVarDeclaration(no.get("varDeclaration"))
            self.visitarVarDeclarationList(no.get("prox"))

    def visitarVarDeclaration(self, no):
        #Tem que tratar do nó interno Indentifierlist
        noIdentifier = no.get("identifierList")
        self.saida += self.simboloTab * self.numTabs + "let "  # Usando "let" para todas as declarações
        while noIdentifier: 
            no.get("id")
            if no.get("prox"):
                self.saida += ", " 
                no.get("prox")
        self.saida += ";\n"

    def visitarBlock(self, noBlock):
        #O método trata dos nós internos Statementlist, Statement, AssignStatement, IfStatement, whilestatement, repeatStatement e commandstatement.
        self.saida += self.simboloTab * self.numTabs + "{\n"
        self.numTabs += 1
        noStatementList = noBlock.get("statementList")
        while noStatementList:
            noStatement = noBlock.get("statement")
            if noStatement == "assignStatement":
                self.saida += self.simboloTab * self.numTabs
                noStatement.get("id")
                self.saida += " = "
                self.visitarInputStatement(noBlock.get("input_statement"))
                self.visitarExpression(noBlock.get("expression"))
                self.saida += ";\n"
            elif noStatement == "ifStatement":
                self.saida += self.simboloTab * self.numTabs + "if ("
                self.visitarExpression(noBlock.get("expression"))
                self.saida += ") "
                self.visitarBlock(noBlock.get("blockIf"))
                if noBlock.get("blockElse"):
                    self.saida += self.simboloTab * self.numTabs + "else "
                    self.visitar(noBlock.get("blockElse"))
            elif noStatement == "whileStatement":
                self.saida += self.simboloTab * self.numTabs + "while ("
                self.visitarExpression(noBlock.get("expression"))
                self.saida += ") "
                self.visitarBlock(noBlock.get("block"))
            elif noStatement == "repeatStatement":
                self.saida += self.simboloTab * self.numTabs + "for (let i = 0; i < "
                self.visitarExpression(noBlock.get("expression"))
                self.saida += "; i++) "
                self.visitarBlock(noBlock.get("block"))
            elif noStatement == "commandStatement":
                self.visitarCommandStatement(noBlock.get("command_statement"))
            noStatementList = noStatementList.get("prox")
        self.varTemp = 0
        self.numTabs -= 1
        self.saida += self.simboloTab * self.numTabs + "}\n"

    
    def visitarInputStatement(self, noIn):
        func = noIn.get("func")
        if func in ["ler_numero", "ler_binario"]:
            self.saida += f"parseInt(prompt("
            self.visitar(noIn.get("string"))
            self.saida += "))"
        elif func == "ler":
            self.saida += "prompt()"
        elif func == "consultar":
            self.saida += "consult()"
        elif func == "criar_figura":
            self.saida += "createFigure("
            self.visitar(noIn.get("args"))
            self.saida += ")"
        elif func == "criar_imagem":
            self.saida += "createImage("
            self.visitar(noIn.get("args"))
            self.saida += ")"
        elif func == "colidiu":
            self.saida += "collided("
            self.visitar(noIn.get("args"))
            self.saida += ")"
        elif func == "aleatorio":
            self.saida += "random("
            self.visitar(noIn.get("args"))
            self.saida += ")"
    def gerarJS(self):
        codigo=self.arvore
        inicio_var = codigo.find('var\n')
        if inicio_var != -1:
            codigo = codigo[inicio_var:]
        
        # Ajustar sintaxe para JavaScript
        codigo = codigo.replace('var', '')
        codigo = codigo.replace('numero', 'let')
        codigo = codigo.replace('texto', 'let')
        codigo=codigo.replace(':','=')
        
        # Ajustar atribuições e estrutura de controle
        codigo = codigo.replace('se (', 'if (')
        codigo = codigo.replace('senao {', 'else {')
        
        # Substituir laço de repetição
        codigo = codigo.replace('repita(3)', 'for (let i = 0; i <3; i++)')

        return codigo
    def visitarCommandStatement(self, noCommand):
        func = noCommand.get("func")
        self.saida += self.simboloTab * self.numTabs
        if func == "mostrar":
            self.saida += "console.log("
            self.visitar(noCommand.get("args")[0])
            self.saida += ");\n"
        elif func == "limpar":
            self.saida += "clear();\n"
        elif func == "inicializar_com_cor":
            self.saida += "initializeWithColor("
            self.visitar(noCommand.get("args")[0])
            self.saida += ");\n"
        elif func == "inicializar_com_imagem":
            self.saida += "initializeWithImage("
            self.visitar(noCommand.get("args")[0])
            self.saida += ");\n"
        elif func == "redefinir_figura":
            self.saida += "resetFigure("
            self.visitar(noCommand.get("args"))
            self.saida += ");\n"
        elif func == "redefinir_imagem":
            self.saida += "resetImage("
            self.visitar(noCommand.get("args")[0])
            self.saida += ");\n"
        elif func == "mover":
            self.saida += "move("
            self.visitar(noCommand.get("args"))
            self.saida += ");\n"
        elif func == "destacar":
            self.saida += "highlight("
            self.visitar(noCommand.get("args")[0])
            self.saida += ");\n"
        elif func == "reverter_destaque":
            self.saida += "revertHighlight();\n"
        elif func == "tocar":
            self.saida += "play("
            self.visitar(noCommand.get("args")[0])
            self.saida += ");\n"
        elif func == "esperar":
            self.saida += "wait("
            self.visitar(noCommand.get("args")[0])
            self.saida += ");\n"
        else:
            raise ValueError(f"Comando desconhecido: {func}")

    #Professor recomendou que o método SumExpression existisse, mas ele apenas retornaria o resultaddoo do Factor.
    def visitarExpression(self, noEx):
        self.visitarSumExpression(noEx.get("sum_expression"))

    def visitarSumExpression(self, noSum):
        self.visitarFactor(noSum.get('factor'))
        
    def visitarFactor(self, noF):
        if noF.op == "id":
            self.saida += noF.valor
        elif noF.op == "num":
            self.saida += noF.valor
        elif noF.op == "bool":
            self.saida += noF.valor.lower()
        elif noF.op == "str":
            self.saida += f'"{noF.valor}"'
        elif noF.op == "PLUS":
            self.saida += "+"
            self.visitar(noF.get("factor"))
        elif noF.op == "MINUS":
            self.saida += "-"
            self.visitar(noF.get("factor"))
        elif noF.op == "NAO":
            self.saida += "!"
            self.visitar(noF.get("factor"))
        elif noF.op == "LPAR":
            self.saida += "("
            self.visitar(noF.get("expression"))
            self.saida += ")"

        
