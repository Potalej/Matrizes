class Matrizes:
    '''A classe Matrizes contém métodos que fazem cálculos envolvendo matrizes, como:
    -> Inversa;
    -> Transposta;
    -> Potência;
    -> etc.'''
    # geradores
    def matrizIdentidade(self, tamanho):
        '''Gera uma matriz identidade com um dado tamanho.'''
        m = [
            [0 if j!= i else 1 for j in range(tamanho)] for i in range(tamanho)
        ]
        return m
        
    # unários
    def transposta(self, matriz):
        '''A transposta de uma matriz é trocar cada elemento a_{ij} por a_{ji}.'''
        linhas, colunas = len(matriz), len(matriz[0])
        matrizTransposta = []
        for i in range(colunas):
            linhaTransposta = [matriz[j][i] for j in range(linhas)]
            matrizTransposta.append(linhaTransposta)
        return matrizTransposta

    def cofator(self, matriz, ponto):
        '''Um cofator de uma matriz é C_{i,j} = (-1)^{i+j} M_{i,j}, onde M_{i,j} é a determinante da matriz original sem o elemento ij.'''
        # matriz cofator
        M = []
        for i in range(0, len(matriz)):
            l = []
            for j in range(0, len(matriz)):
            # pega todos os elementos que não têm linha i e coluna j
                if i != ponto[0] and j != ponto[1]:
                    l.append(matriz[i][j])
            # no caso em que é a_{ixj}, a linha fica vazia, então a gente ignora ela
            if len(l) != 0: M.append(l)
        # tenta calcular a determinante utilizando decomposição LU. Se der algo errado (elemento nulo), então usa Laplace.
        determinante = self.determinante(M)

        return (-1)**(sum(ponto))*determinante

    def decomposicao(self, matriz):
        '''Decompõe a matriz em LU.'''

        tamanho = len(matriz)
        L = self.matrizIdentidade(tamanho)
        U = [[coluna for coluna in linha] for linha in matriz] # copia a matriz sem interferir na original
        for coluna in range(0, len(matriz)-1):
            for linha in range(coluna+1, len(matriz)):
                # L_{ij} = U_{ij}/U_{jj}  
                L[linha][coluna] = U[linha][coluna]/U[coluna][coluna]
                for c in range(coluna, len(matriz)):
                    # U_{ic} -= L_{ij}*U_{jc}
                    U[linha][c] -= L[linha][coluna]*U[coluna][c]

        return [L, U]

    def determinante(self, matriz):
        try: det = self.determinanteLU(matriz)
        except: det = self.determinanteLaplace(matriz)
        return det

    def determinanteLU(self, matriz):
        '''O cálculo de uma matriz triangulada - decomposta em LU, por exemplo -, é o produto de seus elementos diagonais.
        Este método decompõe a matriz e calcula o determinante de U.'''
        U = self.decomposicao(matriz)[1]
        det = 1
        for i in range(0, len(U)):
            det *= U[i][i]
        return det

    def determinanteLaplace(self, matriz):
        '''Cálculo da determinante se utilizando do método de Laplace.'''
        # a determinante usando o método de Laplace utiliza os cofatores
        # se for uma matriz 2x2, a determinante é esse produto básico
        if len(matriz) == 2:
            return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]

        # se for uma matriz maior que 2x2, aí tem um produto entre certos elementos pela determinante de seus cofatores
        det = 0
        for i in range(len(matriz)):
            det += matriz[i][0]*self.cofator(matriz, [i, 0])
        return det
    
    def adjunta(self, matriz):
        '''A adjunta de uma matriz é a transposta da matriz de cofatores.'''
        M = []
        for i in range(len(matriz)):
            linha = []
            for j in range(len(matriz)):
                linha.append(self.cofator(matriz, [i, j]))
            M.append(linha)
        return self.transposta(M)

    def inversa(self, matriz):
        '''A matriz inversa pode ser calculada como o produto do inverso da determinante da matriz pela adjunta da matriz original, isto é, adj(A)/det(A).
        Por isso, se a determinante for zero, a inversa não existe, então já se retorna False.'''

        determinante = self.determinante(matriz)
        
        if determinante == 0: return False

        matrizAdjunta = self.adjunta(matriz)
        inversa = self.produtoPorEscalar(1/determinante, matrizAdjunta)

        return inversa

    # binários
    def produtoPorEscalar(self, escalar, matriz):
        '''O produto de uma matriz por um escalar é o produto de cada elemento da matriz pelo escalar.'''
        matrizProduto = [
            [escalar*coluna for coluna in linha] for linha in matriz
        ]
        return matrizProduto

    def soma(self, m1, m2):
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise(ValueError('As matrizes precisam ter o mesmo tamanho!'))
        matrizSoma = [
            [m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))
        ]
        return matrizSoma