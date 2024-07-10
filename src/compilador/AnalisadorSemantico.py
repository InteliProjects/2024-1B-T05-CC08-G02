from collections import defaultdict
from ClassesAuxiliares import SemanticException, Token

# -*- coding: utf-8 -*-

from ClassesAuxiliares import NoTabela, SemanticException

class AnalisadorSemantico:
    def __init__(self, arvoreSintatica):
        self.arvore = arvoreSintatica  # Recebe a árvore sintática
        self.tabela = {}  # Tabela de símbolos para armazenar informações sobre identificadores

    # Método principal para iniciar a análise semântica
    def analisar(self):
        self.visitarPrograma()  # Método inicial de análise

    # Visita o nó "programa" na árvore sintática
    def visitarPrograma(self):
        id_node = self.arvore.get("id")  # Obtém o nó "id" da árvore
        self.tabela[id_node.valor] = NoTabela(valor=None, tipo="programa")  # Adiciona o programa à tabela de símbolos
        self.visitarDeclarations(self.arvore.get("declarations"))  # Visita as declarações
        self.visitarBlock(self.arvore.get("block"))  # Visita o bloco principal do programa

    # Visita a lista de declarações na árvore sintática
    def visitarDeclarations(self, noDeclarations):
        var_declaration_list_node = noDeclarations.get("varDeclarationList")
        while var_declaration_list_node:
            self.visitarVarDeclaration(var_declaration_list_node.get("varDeclaration"))
            var_declaration_list_node = var_declaration_list_node.get("prox")

    # Visita uma declaração de variável na árvore sintática
    def visitarVarDeclaration(self, noVarDeclaration):
        identifier_list_node = noVarDeclaration.get("identifierList")
        while identifier_list_node:
            identifier_node = identifier_list_node.get("id")
            # Verifica se o identificador já foi declarado
            if identifier_node.valor in self.tabela:
                raise SemanticException(f'O identificador "{identifier_node.valor}" na linha {identifier_node.linha} foi declarado anteriormente')

            # Adiciona o identificador à tabela de símbolos com seu tipo
            self.tabela[identifier_node.valor] = NoTabela(valor=None, tipo=noVarDeclaration.get("type").valor)
            identifier_list_node = identifier_list_node.get("prox")

    # Visita o bloco principal do programa na árvore sintática
    def visitarBlock(self, noBlock):
        statement_list_node = noBlock.get("statementList")
        while statement_list_node:
            statement_node = statement_list_node.get("statement")
            # Verifica o tipo de declaração
            if statement_node.op == "assignStatement":
                id_node = statement_node.get("id")
                # Verifica se o identificador foi declarado
                if id_node.valor not in self.tabela:
                    raise SemanticException(f'O identificador "{id_node.valor}" na linha {id_node.linha} não foi declarado')
                
                # Verifica se a expressão atribuída tem o tipo correto
                expression_node = statement_node.get("expression")
                if expression_node:
                    visitar_expression = self.visitarExpression(expression_node)
                    if self.tabela[id_node.valor].tipo != visitar_expression.tipo:
                        raise SemanticException(f'O identificador "{id_node.valor}" na linha {id_node.linha} não pode receber uma expressão do tipo "{visitar_expression.tipo}"')
                self.tabela[id_node.valor].valor = id_node.valor
                
            elif statement_node.op == "outStatement":
                self.visitarExpression(statement_node.get("expression"))
                
            elif statement_node.op == "ifStatement":
                self.visitarBlock(statement_node.get("blockIf"))
                if statement_node.get("blockElse"):
                    self.visitarBlock(statement_node.get("blockElse"))
                    
            statement_list_node = statement_list_node.get("prox")
    
    # Visita uma expressão na árvore sintática
    def visitarExpression(self, noExpression):
        esq_node = noExpression.get("esq")
        result = self.visitarSumExpression(esq_node)
        oper_node = noExpression.get("oper")
        if oper_node:
            dir_node = noExpression.get("dir")
            return NoTabela(valor=self.visitarSumExpression(dir_node), tipo="binario")
        return result

    # Visita uma expressão de soma na árvore sintática
    def visitarSumExpression(self, no):
        if no != None:
            val1 = self.visitarSumExpression(no.get("esq"))
            val2 = self.visitarSumExpression(no.get("dir"))
            oper_node = no.get("oper")

            if val1.tipo != val2.tipo:
                raise SemanticException(f'Tipos incompatíveis: "{val1.valor}" e "{val2.valor}"')
            elif oper_node == '/' and val2.tipo == "numero" and val2.valor == 0:
                raise SemanticException(f'Divisão por 0 na linha {val2.get("linha")}')
            elif oper_node == '^' and val2.tipo == "numero" and float(val2.valor) < 0:
                raise SemanticException(f'Expoente negativo na linha {val2.get("linha")}')

            if val1:
                return val1
            return val2
                
        elif no.op == "factor" and not no.get("expression"):
            factor_node = no.get("factor")
            if factor_node.op == "id":
                if factor_node.valor not in self.tabela:
                    raise SemanticException(f'O identificador "{factor_node.valor}" na linha {factor_node.linha} não foi declarado')
                elif self.tabela[factor_node.valor].valor == None:
                    raise SemanticException(f'O identificador "{factor_node.valor}" na linha {factor_node.linha} não foi inicializado')
                else:
                    return self.tabela[factor_node.valor]
            
            elif factor_node.op == "binario":
                return NoTabela(valor=factor_node.valor, tipo="binario")
            
            elif factor_node.op == "numero":
                sinal = no.get("sinal")
                if sinal == "-":
                    negative_num = sinal + factor_node.valor
                    return NoTabela(valor=negative_num, tipo="numero", linha=factor_node.linha)
                return NoTabela(valor=factor_node.valor, tipo="numero")
                
        elif no.op == "factor" and no.get("expression"):
            return self.visitarExpression(no.get("expression"))
    
    # Realiza todas as verificações semânticas necessárias
    def analisa(self):
        self.verifica_duplicata()
        self.verifica_nao_declarado()
        self.verifica_string_indevida()
        self.verifica_url()

    # Retorna uma lista de tokens de variáveis na árvore sintática
    def lista_var(self):
        encontrou_var = False
        tokens_id = []

        for token in self.arvore:
            if encontrou_var:
                if token.tipo == "LBLOCK":
                    break
                elif token.tipo == "ID":
                    tokens_id.append(token)
            elif token.tipo == "VAR":
                encontrou_var = True
        return tokens_id

    # Verifica se há duplicação de identificadores
    def verifica_duplicata(self):
        tokens = self.lista_var()
        tokens_vistos = set()
        for token in tokens:
            if (token.tipo, token.valor) in tokens_vistos:
                raise SemanticException(f"O identificador '{token.valor}' na linha '{token.linha}' foi declarado anteriormente")
            else:
                tokens_vistos.add((token.tipo, token.valor))
        return None

    # Verifica se todos os identificadores foram declarados
    def verifica_nao_declarado(self):
        tokens_declarados = self.lista_var()
        print(tokens_declarados)
        for token in self.arvore:
            if token.tipo == "ID" and token.valor not in {t.valor for t in tokens_declarados}:
                raise SemanticException(f"O identificador '{token.valor}' na linha '{token.linha}' não foi declarado")

    # Verifica se uma variável está tentando receber uma string indevidamente
    def verifica_string_indevida(self):  
        for i in range(0, len(self.arvore) - 1):
            if self.arvore[i].tipo == "ID" and self.arvore[i + 1].tipo == "ASSIGN" and self.arvore[i + 2].tipo == "DQUOTE":
                raise SemanticException(f"O identificador '{self.arvore[i].valor}' na linha '{self.arvore[i].linha}' não pode receber uma expressão do tipo texto")
    
    # Verifica se um arquivo é uma URL válida
    def verifica_url(self):
        for i in range(0, len(self.arvore) - 1):
            if self.arvore[i].valor=="criar_imagem" or self.arvore[i].valor=="inicializar_com_imagem" or self.arvore[i].valor=="redefinir_imagem" or self.arvore[i].valor=="tocar":
                i+=3
                if "/" in self.arvore[i].valor or not("." in self.arvore[i].valor):
                    raise SemanticException(f"O arquivo '{self.arvore[i].valor}', na linha '{self.arvore[i].linha}', não pode estar dentro de uma subpasta e deve ter uma extensão.")