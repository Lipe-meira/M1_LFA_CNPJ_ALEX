# Usa AFD (automato finito deterministico).
#
# Padrao: AA.AAA.AAA/AAAA-DV
#   A  = 0-9 ou A-Z
#   DV = dois digitos (0-9)
#
# Autores: Nilson Felipe Meira e Andrey Marques

import os
from CapturaRecursosWeb import CapturaRecursosWeb

DIGITOS = "0123456789"
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
QUANTIDADEESTADOS = 19


def getCharRef(alfabeto, simbolo):
    """Procura o simbolo no alfabeto e devolve o indice da coluna da matriz."""
    for indice in range(len(alfabeto)):
        if alfabeto[indice] == simbolo:
            return indice
    return -1


def getStringRef(listaEstados, nomeEstado):
    """Procura o nome do estado (q0, q1, ...) e devolve o indice da linha."""
    for indice in range(len(listaEstados)):
        if listaEstados[indice] == nomeEstado:
            return indice
    return -1


def proximoEstado(alfabeto, matriz, estadoAtual, simbolo):
    """Olha a matriz e diz para qual estado ir depois de ler o simbolo."""
    coluna = getCharRef(alfabeto, simbolo)
    if coluna != -1:
        return matriz[estadoAtual][coluna]
    return -1


def transicaoAlfanumerico(alfabeto, estados, matriz, estadoOrigem, estadoDestino):
    """Liga dois estados para letra ou numero. Usado nas 12 primeiras posicoes."""
    origem = getStringRef(estados, estadoOrigem)
    destino = getStringRef(estados, estadoDestino)

    for digito in DIGITOS:
        coluna = getCharRef(alfabeto, digito)
        matriz[origem][coluna] = destino

    for letra in LETRAS:
        coluna = getCharRef(alfabeto, letra)
        matriz[origem][coluna] = destino


def transicaoDigito(alfabeto, estados, matriz, estadoOrigem, estadoDestino):
    """Liga dois estados so para numero (0-9). Usado nos 2 digitos do DV."""
    origem = getStringRef(estados, estadoOrigem)
    destino = getStringRef(estados, estadoDestino)

    for digito in DIGITOS:
        coluna = getCharRef(alfabeto, digito)
        matriz[origem][coluna] = destino


def transicaoSimbolo(alfabeto, estados, matriz, estadoOrigem, simbolo, estadoDestino):
    """Liga dois estados para um simbolo da mascara: ponto, barra ou hifen."""
    origem = getStringRef(estados, estadoOrigem)
    coluna = getCharRef(alfabeto, simbolo)
    destino = getStringRef(estados, estadoDestino)
    matriz[origem][coluna] = destino


def reconhecer(texto, alfabeto, estados, estadoInicial, estadosFinais, matriz):
    """Percorre o HTML letra a letra. Se chega em q18, guarda o CNPJ."""
    estado = getStringRef(estados, estadoInicial)
    estadoAnterior = -1
    encontrados = []
    palavra = ""

    indice = 0
    while indice < len(texto):
        simbolo = texto[indice]
        estadoAnterior = estado
        estado = proximoEstado(alfabeto, matriz, estado, simbolo)

        if estado == -1:
            estado = getStringRef(estados, estadoInicial)
            chegouNoFinal = getStringRef(estadosFinais, estados[estadoAnterior]) != -1
            if chegouNoFinal:
                if palavra != "":
                    encontrados.append(palavra)
                indice = indice - 1
            palavra = ""
        else:
            palavra = palavra + simbolo

        indice = indice + 1

    chegouNoFinal = getStringRef(estadosFinais, estados[estado]) != -1
    if chegouNoFinal and palavra != "":
        encontrados.append(palavra)

    return encontrados


def possuiLetra(texto):
    """Devolve True se o CNPJ tem alguma letra (alfanumerico)."""
    for indice in range(len(texto)):
        simbolo = texto[indice]
        if simbolo >= "A" and simbolo <= "Z":
            return True
    return False


def baixarHtml(urlWeb, urlLocal):
    """Baixa o HTML da internet. Se falhar, le a copia local."""
    captura = CapturaRecursosWeb()
    captura.getListaRecursos().append(urlWeb)
    paginas = captura.carregarRecursos()

    if len(paginas) > 0:
        html = paginas[0]
        if html is not None and html != "":
            return html

    print("[aviso] Sem acesso a " + urlWeb + " — usando copia local.")
    captura = CapturaRecursosWeb()
    captura.getListaRecursos().append(urlLocal)
    paginas = captura.carregarRecursos()
    if len(paginas) > 0:
        return paginas[0]
    return ""


def criarAlfabeto():
    """Monta o alfabeto do AFD: 0-9, A-Z, ponto, barra e hifen."""
    alfabeto = []
    for digito in DIGITOS:
        alfabeto.append(digito)
    for letra in LETRAS:
        alfabeto.append(letra)
    alfabeto.append(".")
    alfabeto.append("/")
    alfabeto.append("-")
    return alfabeto


def criarEstados():
    """Cria os estados q0 (inicio) ate q18 (CNPJ completo)."""
    estados = []
    for numeroEstado in range(QUANTIDADEESTADOS):
        estados.append("q" + str(numeroEstado))
    return estados


def criarMatrizVazia(quantidadeEstados, tamanhoAlfabeto):
    """Cria a tabela cheia de -1 (ainda sem nenhum caminho)."""
    matriz = []
    for linha in range(quantidadeEstados):
        colunas = []
        for coluna in range(tamanhoAlfabeto):
            colunas.append(-1)
        matriz.append(colunas)
    return matriz


def criarMatriz(alfabeto, estados):
    """Preenche os caminhos do padrao AA.AAA.AAA/AAAA-DV."""
    matriz = criarMatrizVazia(len(estados), len(alfabeto))

    # AA .
    transicaoAlfanumerico(alfabeto, estados, matriz, "q0", "q1")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q1", "q2")
    transicaoSimbolo(alfabeto, estados, matriz, "q2", ".", "q3")

    # AAA .
    transicaoAlfanumerico(alfabeto, estados, matriz, "q3", "q4")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q4", "q5")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q5", "q6")
    transicaoSimbolo(alfabeto, estados, matriz, "q6", ".", "q7")

    # AAA /
    transicaoAlfanumerico(alfabeto, estados, matriz, "q7", "q8")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q8", "q9")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q9", "q10")
    transicaoSimbolo(alfabeto, estados, matriz, "q10", "/", "q11")

    # AAAA -
    transicaoAlfanumerico(alfabeto, estados, matriz, "q11", "q12")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q12", "q13")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q13", "q14")
    transicaoAlfanumerico(alfabeto, estados, matriz, "q14", "q15")
    transicaoSimbolo(alfabeto, estados, matriz, "q15", "-", "q16")

    # DV (q18 aceita o CNPJ)
    transicaoDigito(alfabeto, estados, matriz, "q16", "q17")
    transicaoDigito(alfabeto, estados, matriz, "q17", "q18")

    return matriz


def exibirResultados(numeroPagina, url, encontrados):
    """Mostra no console os CNPJs achados em uma pagina."""
    print("")
    print("--- Pagina " + str(numeroPagina) + " ---")
    print("URL: " + url)
    print("Itens encontrados: " + str(len(encontrados)))

    if len(encontrados) == 0:
        print("  (nenhum CNPJ no padrao AA.AAA.AAA/AAAA-DV)")
        return

    for indice in range(len(encontrados)):
        item = encontrados[indice]
        if possuiLetra(item):
            tipo = "alfanumerico"
        else:
            tipo = "numerico"
        print("  " + str(indice + 1) + ") " + item + "  [" + tipo + "]")


def main():
    """Monta o AFD, baixa 3 paginas e lista os CNPJs de cada uma."""
    urls = []
    urls.append("https://www.samsung.com/br/")
    urls.append("https://g1.globo.com/empreendedorismo/noticia/2026/08/01/receita-federal-emite-o-primeiro-cnpj-alfanumerico-do-brasil-entenda-o-que-muda.ghtml")
    urls.append("https://batedor.com.br/blog/cnpj-alfanumerico-novo-formato")
    urls.append("https://www.kabum.com.br/sobre")

    pastaPython = os.path.dirname(os.path.abspath(__file__))
    pastaRaiz = os.path.join(pastaPython, "..")
    urlLocal = os.path.join(pastaRaiz, "paginas", "cnpj-alfanumerico.html")

    alfabeto = criarAlfabeto()
    estados = criarEstados()
    estadoInicial = "q0"
    estadosFinais = ["q18"]
    matriz = criarMatriz(alfabeto, estados)

    print("==============================================")
    print(" Busca de CNPJ alfanumerico (AFD)")
    print(" Padrao: AA.AAA.AAA/AAAA-DV")
    print("==============================================")

    totalGeral = 0
    for indicePagina in range(len(urls)):
        html = baixarHtml(urls[indicePagina], urlLocal)
        html = html.upper()

        encontrados = reconhecer(
            html, alfabeto, estados, estadoInicial, estadosFinais, matriz
        )

        exibirResultados(indicePagina + 1, urls[indicePagina], encontrados)
        totalGeral = totalGeral + len(encontrados)

    print("")
    print("==============================================")
    print(" Total geral: " + str(totalGeral) + " item(ns)")
    print("==============================================")


if __name__ == "__main__":
    main()
