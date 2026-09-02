# Busca de CNPJ Alfanumérico com AFD

Projeto desenvolvido para a disciplina de Linguagens Formais e Autômatos. O programa utiliza um Autômato Finito Determinístico (AFD) para localizar CNPJs numéricos e alfanuméricos no código HTML de páginas da Web.

A busca é realizada caractere por caractere, sem utilização de bibliotecas de expressão regular.

## Padrão reconhecido

O programa reconhece CNPJs no formato:

```text
AA.AAA.AAA/AAAA-DD
```

Onde:

* `A` representa uma letra de `A-Z` ou um número de `0-9`;
* `D` representa somente um número de `0-9`;
* os símbolos `.`, `/` e `-` devem aparecer nas posições corretas.

Exemplos aceitos:

```text
12.ABC.345/01DE-35
00.280.273/0001-37
XP.TO1.234/0001-20
```

Expressão regular equivalente:

```regex
[0-9A-Z]{2}\.[0-9A-Z]{3}\.[0-9A-Z]{3}/[0-9A-Z]{4}-[0-9]{2}
```

## Funcionamento

O programa executa as seguintes etapas:

1. Cria o alfabeto com números, letras e símbolos;
2. Cria os estados `q0` até `q18`;
3. Monta a matriz de transição do AFD;
4. Baixa o HTML das páginas selecionadas;
5. Percorre o HTML caractere por caractere;
6. Consulta a matriz para descobrir o próximo estado;
7. Quando o estado final `q18` é alcançado, armazena o CNPJ encontrado;
8. Exibe os resultados no console.

A matriz representa a tabela de transição do autômato. Entradas inválidas recebem o valor `-1`, fazendo a busca retornar ao estado inicial.

## Páginas analisadas

O programa realiza a busca nas seguintes páginas:

* Samsung Brasil;
* G1;
* Batedor;
* KaBuM!.

Caso não seja possível acessar uma página, o programa utiliza uma cópia HTML salva localmente.

## Estrutura do projeto

```text
M1_LFA_CNPJ_ALEX/
├── python/
│   ├── main.py
│   └── CapturaRecursosWeb.py
├── paginas/
│   └── cnpj-alfanumerico.html
├── AtividadeM1LFA.pdf
├── LFA_CNPJ_Alfanumerico_Com_Implementacao_Atualizado.docx
├── Slides_LFA_M1_CNPJ.pptx
└── README.md
```

### `main.py`

Responsável por:

* criar o alfabeto e os estados;
* construir a matriz de transição;
* executar o AFD;
* reconhecer os CNPJs;
* exibir os resultados.

### `CapturaRecursosWeb.py`

Responsável por:

* baixar o HTML das páginas;
* configurar a requisição Web;
* ler a cópia HTML local;
* tratar falhas de conexão.

## Requisitos

* Python 3;
* conexão com a internet para acessar as páginas.

O projeto utiliza somente bibliotecas nativas do Python, portanto não é necessário instalar dependências externas.

## Como executar

Clone o repositório:

```bash
git clone https://github.com/Lipe-meira/M1_LFA_CNPJ_ALEX.git
```

Entre na pasta do programa:

```bash
cd M1_LFA_CNPJ_ALEX/python
```

Execute:

```bash
python main.py
```

No Windows também é possível utilizar:

```bash
py main.py
```

## Exemplo de saída

```text
==============================================
 Busca de CNPJ alfanumerico (AFD)
 Padrao: AA.AAA.AAA/AAAA-DV
==============================================

--- Pagina 1 ---
URL: https://www.samsung.com/br/
Itens encontrados: 1
  1) 00.280.273/0001-37 [numerico]
```

A quantidade de resultados pode mudar conforme o conteúdo das páginas é atualizado.

## Observação

O programa verifica se o texto pertence ao formato definido pelo AFD. Ele não realiza o cálculo matemático dos dígitos verificadores do CNPJ.

## Autores

* Nilson Roffman
* Felipe Meira
* Andrey Marques
