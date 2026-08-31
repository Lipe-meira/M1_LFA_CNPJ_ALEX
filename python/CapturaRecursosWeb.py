
import urllib.request

class CapturaRecursosWeb:
    def __init__(self):
        self.listaRecursos = []

    def getListaRecursos(self):
        """Devolve a lista de URLs que serao baixadas."""
        return self.listaRecursos

    def lerArquivoLocal(self, caminho):
        """Le um HTML salvo na pasta do projeto."""
        arquivo = open(caminho, "r", encoding="utf-8")
        html = arquivo.read()
        arquivo.close()
        return html

    def baixarPaginaWeb(self, url):
        """Baixa o codigo-fonte HTML de uma pagina da internet."""
        pedido = urllib.request.Request(url)
        pedido.add_header("User-Agent", "Mozilla/5.0")
        conexao = urllib.request.urlopen(pedido, timeout=15)
        htmlBytes = conexao.read()
        html = htmlBytes.decode("utf-8", errors="ignore")
        conexao.close()
        return html

    def carregarRecursos(self):
        """Percorre a lista de URLs e devolve o HTML de cada uma."""
        resultado = []

        for url in self.listaRecursos:
            try:
                ehWeb = url.startswith("http://") or url.startswith("https://")
                if ehWeb:
                    html = self.baixarPaginaWeb(url)
                else:
                    html = self.lerArquivoLocal(url)
                resultado.append(html)
            except Exception as erro:
                print(erro)

        return resultado
