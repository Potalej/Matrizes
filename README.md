# 🧮 Matrizes

🎓 Aqui estão alguns métodos que fazem operações com matrizes. 

🌞 Os métodos foram divididos entre geradores (não envolvem nenhuma matriz à priori), unários (envolvem só uma matriz) ou binários (envolvem duas matrizes). 

👨‍💻O código está em construção, então alguns métodos ainda hão de ser escritos e adicionados!

<hr>

<h2>📌Sumário</h2>

* [Métodos Geradores](#metodos-geradores)
  * [Identidade](#identidade)
* [Métodos Unários](#metodos-unarios)
  * [Transposta](#transposta)
  * [Cofator](#cofator)
  * [Decomposição LU](#decomplu)
  * [Determinante](#determinante)
    * [Por Decomposição LU](#determinantelu)
    * [Pelo Método de Laplace](#determinantelaplace)
  * [Adjunta](#adjunta)
  * [Inversa](#inversa)
* [Métodos Binários](#metodos-binarios)
  * [Produto por Escalar](#escalar) 
  * [Soma](#soma)

<hr>

<h2 id="#metodos-geradores">Métodos Geradores</h2>

<h3 id="#identidade">Identidade</h3>

O método que gera matrizes identidade recebe somente um tamanho e gera uma matriz identidade se gerando uma matriz nula com tal tamanho e tornando 1 a diagonal.

```python
m = [
    [0 if j!= i else 1 for j in range(tamanho)] for i in range(tamanho)
]
return m
```

<h2 id="#metodos-unarios">Métodos Unários</h2>

<h3 id="#transposta">Transposta</h3>

A transposta de uma matriz é, para todo elemento na linha i e coluna j, pô-lo na posição de linha j e coluna i.

```python
linhas, colunas = len(matriz), len(matriz[0])
matrizTransposta = []
for i in range(colunas):
    linhaTransposta = [matriz[j][i] for j in range(linhas)]
    matrizTransposta.append(linhaTransposta)
return matrizTransposta
```

<h3 id="cofator">Cofator</h3>

Um cofator de uma matriz é C_{i,j} = (-1)^{i+j} M_{i,j}, onde M_{i,j} é a determinante da matriz original sem o elemento ij. É utilizado tanto no cálculo da determinante pelo método de Laplace quanto no cálculo da matriz inversa pelo método da adjunta.

```python
M = []
for i in range(0, len(matriz)):
    l = []
    for j in range(0, len(matriz)):
    # pega todos os elementos que não têm linha i e coluna j
        if i != ponto[0] and j != ponto[1]:
            l.append(matriz[i][j])
    # no caso em que é a_{ixj}, a linha fica vazia, então se ignora ela
    if len(l) != 0: M.append(l)
# tenta calcular a determinante utilizando decomposição LU. 
# Se der algo errado (elemento nulo), então usa Laplace.
determinante = self.determinante(M)

return (-1)**(sum(ponto))*determinante
```

O método da determinante será apresentado mais à frente.

<h3 id="decomplu">Decomposição LU</h3>

A decomposição LU aqui é utilizada para agilizar o cálculo de determinantes. A decomposição é feita se utilizando de pivoteamento, e o retorno se dá em duas matrizes, uma triangulada pela esquerda inferior e outra pela direita superior.

```python
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
```

Por nem sempre ser possível fazer o pivoteamento (já que eventualmente algum elemento da diagonal de uma matriz pode ser ou vir a se tornar nulo), a decomposição nem sempre funciona, mas isto é tratado na determinante.

<h3 id="determinante">Determinante</h3>

O cálculo de uma determinante é um processo que para matrizes pequenas não gera tanto trabalho computacional, mas para grandes matrizes pode ser um processo muito custoso dependendo do método utilizado.

Por enquanto, são utilizados os métodos da determinante por Decomposição LU e o de Laplace. Na hora do cálculo, o método tenta o efetuar pelo método da decomposição, e se houver algum erro o faz com o de Laplace.

```python
try: det = self.determinanteLU(matriz)
except: det = self.determinanteLaplace(matriz)
return det
```

<h4 id="determinantelu">Por Decomposição LU</h4>

O cálculo de uma determinante se utilizando do método da decomposição LU se dá no produto dos elementos diagonais de U, e por isso a velocidade de cálculo muito superior ao que vem a ser utilizado no cálculo da determinante pelo método de Laplace.

```python
U = self.decomposicao(matriz)[1]
det = 1
for i in range(0, len(U)):
    det *= U[i][i]
return det
```

<h4 id="determinantelaplace">Pelo Método de Laplace</h4>

O cálculo de uma determinante pelo método de Laplace envolve multiplicar cada elemento de uma linha ou coluna selecionada pelo seu cofator - e por isso o custo para grandes matrizes.

```python
# a determinante usando o método de Laplace utiliza os cofatores
# se for uma matriz 2x2, a determinante é esse produto básico
if len(matriz) == 2:
    return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]

# se for uma matriz maior que 2x2, aí tem um produto entre certos elementos pela determinante de seus cofatores
det = 0
for i in range(len(matriz)):
    det += matriz[i][0]*self.cofator(matriz, [i, 0])
return det
```

<h3 id="adjunta">Adjunta</h3>

A adjunta de uma matriz é a transposta da matriz de cofatores de cada elemento da matriz original. Pode ser utilizada no cálculo da inversa.

```python
M = []
for i in range(len(matriz)):
    linha = []
    for j in range(len(matriz)):
        linha.append(self.cofator(matriz, [i, j]))
    M.append(linha)
return self.transposta(M)
```

<h3 id="inversa">Inversa</h3>

A inversa de uma matriz é a matriz tal que o produto dela pela original é a matriz identidade de mesmo tamanho.
Há algumas formas de se calcular essa matriz, mas a utilizada aqui se dá através do produto da matriz adjunta pelo inversa da determinante da matriz original. Essa operação é binária e é determinada mais à frente.

```python
determinante = self.determinante(matriz)

if determinante == 0: return False

matrizAdjunta = self.adjunta(matriz)
inversa = self.produtoPorEscalar(1/determinante, matrizAdjunta)

return inversa
```

Se a determinante da matriz é nula, ela não possui inversa, e por isso se retorna False.

<h2 id="metodos-binarios">Métodos Binários</h2>
<h3 id="escalar">Produto por Escalar</h3>
O produto de uma matriz por um escalar é o produto de cada elemento da matriz pelo escalar, isto é:

```python
matrizProduto = [
    [escalar*coluna for coluna in linha] for linha in matriz
]
return matrizProduto
```

<h3 id="soma">Soma</h3>
A soma de duas matrizes é a soma dos elementos correspondentes de cada matriz. Por isso, as matrizes devem ter o mesmo tamanho.

```python
if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
    raise(ValueError('As matrizes precisam ter o mesmo tamanho!'))
matrizSoma = [
    [m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))
]
return matrizSoma
```