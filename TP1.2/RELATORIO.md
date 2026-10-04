# TP1.2 - Sudoku genérico como CSP

## 1. Problema e objetivo

Para um parâmetro `n`, a grelha tem lado `N = n²`. Cada célula deve conter um
inteiro de `1` a `N`. Em cada linha, coluna e bloco regular `n × n`, todos os
valores têm de ser diferentes. O objetivo é encontrar uma solução que satisfaça
estas restrições e as pistas dadas, ou demonstrar que não existe solução. O
enunciado não exige encontrar uma solução única nem otimizar uma função.

O trabalho usa a abordagem da cadeira: declarar variáveis e restrições e pedir
a um solver genérico que encontre uma atribuição válida. A biblioteca escolhida
foi OR-Tools CP-SAT, sugerida pelo professor. O notebook está em Marimo e usa
Python 3.14, como indicado no template.

## 2. Estrutura da solução

O ficheiro principal é `sudoku.py`. O enunciado original foi copiado sem
alterações para `enunciado_professor.py`.

| Componente | Responsabilidade |
|---|---|
| `box(n, cells)` | Guardar um grupo arbitrário de coordenadas e valores fixos ou `None`. `add` valida os limites; `matrix` devolve uma matriz de zeros e valores fixos. |
| `cube(n, i, j)` | Construir o bloco `n × n` cujo canto superior esquerdo é `(i*n, j*n)`. |
| `path(n, inicio, fim)` | Construir um segmento horizontal ou vertical, inclusivo nos dois sentidos. |
| `random_clues(n, k, rng)` | Escolher `k` células distintas e valores aleatórios de `1` a `N`. |
| `SudokuCSP(n)` | Criar as `N²` variáveis inteiras e aplicar `AllDifferent` e as pistas a quaisquer grupos recebidos. |
| `make_sudoku` | Criar as `N` linhas, `N` colunas, `n²` blocos e juntar pistas e grupos opcionais. |
| `validate_solution` | Verificar a solução sem consultar o solver. |

`box` só conhece células: não contém regras específicas de Sudoku, blocos ou
solver. As especializações apenas escolhem coordenadas. A regra `AllDifferent`
é aplicada uma única vez, em `SudokuCSP.add_groups`, independentemente de onde
o grupo veio. Isto permite acrescentar um Sudoku diagonal passando mais dois
grupos `box`, sem mudar o modelo.

### Exemplo pequeno da abstração

Para `n=2`, `path(2, (0,3), (0,0))` contém `(0,3)`, `(0,2)`, `(0,1)` e `(0,0)`.
Para `cube(2,1,1)`, as células são `(2,2)`, `(2,3)`, `(3,2)` e `(3,3)`.
Uma pista como `(0,1) -> 2` é um `box` de uma célula fixa. O modelo trata os
três objetos da mesma forma.

## 3. Modelo de restrições

Para cada coordenada `(i,j)` existe uma variável inteira `x[i,j] ∈ {1,...,N}`.
Para cada grupo `G` recebido, impõe-se `AllDifferent(x[i,j] para (i,j) em G)`.
Se `(i,j)` estiver fixada ao valor `v` nesse grupo, acrescenta-se `x[i,j] = v`.

O Sudoku base passa ao modelo:

- `N` linhas construídas com `path`;
- `N` colunas construídas com `path`;
- `n² = N` blocos construídos com `cube`;
- um grupo `box` com as pistas aleatórias.

Cada linha, coluna e bloco tem exatamente `N` células com domínio de tamanho
`N`. Por isso, `AllDifferent` obriga esses grupos a conter uma permutação de
`1..N`. As igualdades das pistas garantem que a solução as preserva. Estas
duas observações justificam a correção do modelo base.

O solver devolve a grelha quando encontra solução (`OPTIMAL` ou `FEASIBLE`) e
`None` quando prova `INFEASIBLE`. Se não concluir dentro do limite de 10 s, o
notebook lança um erro; `UNKNOWN` não é confundido com impossibilidade.

## 4. Pistas aleatórias e limites da geração

As posições são escolhidas sem repetição; os valores são escolhidos
independentemente. Isto cumpre literalmente o pedido de pistas aleatórias, mas
pode produzir duas pistas iguais na mesma linha ou outro conflito. O modelo
devolve então `None`. Apenas para apresentar um exemplo resolvido, `run_example`
faz nova amostragem até encontrar um conjunto compatível, com no máximo 20
tentativas. A função básica `random_clues` permanece independente do solver.

Poucas pistas geralmente deixam várias soluções possíveis. O trabalho não
afirma que o puzzle gerado seja único. A geração de puzzles únicos seria uma
tarefa adicional: seria preciso procurar uma segunda solução diferente da
primeira e rejeitar o puzzle se ela existisse.

## 5. Validação e resultados

O notebook executa e apresenta grelhas para `n=2` (4×4) e `n=3` (9×9), depois
valida também uma grelha `n=4` (16×16). O teste de 16×16 é uma evidência
limitada de parametrização, não uma garantia de desempenho geral. O notebook
mostra o tempo e o número de ramos medidos pelo solver em cada execução.

`validate_solution` verifica independentemente:

1. dimensões e valores de cada linha;
2. todas as colunas;
3. todos os blocos;
4. cada pista fixa.

Os nove testes em `test_sudoku.py` cobrem ainda coordenadas e valores inválidos,
conflitos numa célula, caminhos nos dois sentidos, índices de bloco, pistas
distintas, um grupo extra, um caso `INFEASIBLE`, rejeição de grupos com outro
`n` e deteção de uma grelha adulterada. Foram executados com Python 3.14.8 e
passaram. O verificador de Marimo também passou, e o notebook foi executado e
exportado para PDF.

## 6. Complexidade

Escrevendo `N=n²`, o modelo base tem `N²=n⁴` variáveis, cada uma com `N`
valores possíveis. Há `3N` grupos principais de tamanho `N`; a enumeração de
grupos e a criação das variáveis custam `O(N²)` em tempo e espaço, sem contar
os detalhes internos do solver. Acrescentar `k` pistas custa `O(k)` depois de
escolher as posições; `box.matrix()` custa `O(N²)` e um `cube` ou `path`
completo custa `O(N)`.

A resolução do CSP domina o custo. Uma enumeração ingénua poderia experimentar
até `N^(N²)` atribuições. A propagação de `AllDifferent` e a pesquisa de CP-SAT
podem reduzir muito esse espaço, mas não oferecem um limite polinomial geral
para as instâncias do problema. Os tempos mostrados são medições locais de
exemplos concretos.

## 7. Decisões e alternativas

- **Dicionário em `box`:** só guarda as células de um grupo. A matriz é criada
  quando é preciso apresentar os dados. Isto mantém `box` simples e reutilizável.
- **`AllDifferent` global:** expressa diretamente a regra da cadeira e evita
  escrever todas as desigualdades por pares.
- **Uma função para montar o Sudoku:** mantém a construção de linhas, colunas
  e blocos separada da implementação do solver.
- **Validador externo ao modelo:** permite detetar um erro de modelação sem
  confiar apenas no estado devolvido pelo solver.
- **Pistas independentes:** cumprem o enunciado, com reporte explícito de
  casos impossíveis. Não são um gerador de puzzles únicos.
- **Semente fixa nos exemplos:** torna as demonstrações reproduzíveis;
  `random_clues` continua a aceitar aleatoriedade normal.
- **Sudoku diagonal:** é uma extensão opcional pequena que demonstra a
  generalidade de `box`; não substitui os requisitos base.

## 8. Como reproduzir e apresentar

Na raiz do repositório, neste PC:

```bash
.venv/bin/marimo edit TP1.2/sudoku.py
.venv/bin/python -m unittest discover -s TP1.2 -v
.venv/bin/marimo check TP1.2/sudoku.py
```

Na apresentação, uma sequência curta e suficiente é:

1. mostrar `box`, `cube` e `path` com um exemplo 4×4;
2. apontar a única chamada a `add_all_different` no modelo;
3. executar os exemplos 4×4 e 9×9 e verificar as pistas;
4. criar duas pistas iguais na mesma linha e mostrar `INFEASIBLE`;
5. acrescentar as duas diagonais e mostrar que o solver não mudou;
6. explicar por que `n=4` funciona sem alterar o código.

É importante conseguir explicar a diferença entre `INFEASIBLE` (prova de que
não há solução), `UNKNOWN` (a pesquisa não concluiu) e solução não única.

## Referências

- Enunciado fornecido pelo professor: `enunciado_professor.py`.
- [OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver/).
- [Marimo: execução e exportação de notebooks](https://docs.marimo.io/guides/scripts/).
- [Marimo: importação de funções e classes de notebooks](https://docs.marimo.io/guides/reusing_functions/).
