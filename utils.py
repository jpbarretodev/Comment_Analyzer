# classe de utilitários pra mexer com os dados
from collections import Counter
import nltk
from nltk.stem.rslp import RSLPStemmer
from elogiosCriticasKeyWords import KeyWords


class Utils(KeyWords):


    def __init__(self, avaliacoes: object):
        super().__init__()
        self.avaliacoes = avaliacoes

        self.quantidadeComentarios = 0
        self.mediaNotas = 0
        self.comentarioLongo = []
        self.comentarioCurto = [] 
        self.tamanhoMedioComentarios = 0
        self.palavraMaisFrequente = ""

        # Informações sobre os comentários
        self.exemploComentariosPositivos = []
        self.exemploComentariosNegativos = []
        self.principaisElogios = []
        self.principaisCriticas = []
        self.estrelas = {}

    def getQuantidadeComentarios(self):
        totalComentarios = []

        for avaliacao in self.avaliacoes:
            totalComentarios.append(avaliacao["content"])

        self.quantidadeComentarios = len(totalComentarios)

        #return len(totalComentarios) # so to fazendo assim pq to com preguiça e sao poucos dados
        
    def getMediaNotas(self):
        totalNotas = len(self.avaliacoes)
        somaNotas = 0

        for avaliacao in self.avaliacoes:
            somaNotas += avaliacao["score"]

        self.mediaNotas = somaNotas / totalNotas

        #return somaNotas / totalNotas

    def getComentarioLongo(self):
        quantidadePalavras = 0
        comentario = ""

        for avaliacao in self.avaliacoes:
            if len(avaliacao["content"]) > quantidadePalavras:
                quantidadePalavras = len(avaliacao["content"])
                comentario = avaliacao["content"]

        self.comentarioLongo = comentario
            
        # return comentario # retorna a lista de palavras do comentario

    def getComentarioCurto(self):
        quantidade = len(self.avaliacoes[0]["content"])
        comentario = self.avaliacoes[0]["content"]

        for avaliacao in self.avaliacoes[1:]:
            if len(avaliacao["content"]) < quantidade:
                quantidade = len(avaliacao["content"])
                comentario = avaliacao["content"]

        self.comentarioCurto = comentario

        #return comentario

    def getTamanhoMedioComentarios(self):
        totalTamanhoComentario = 0

        # recolhendo os tamanhos dos comentarios
        for avaliacao in self.avaliacoes:
            totalTamanhoComentario += len(avaliacao["content"])

        self.tamanhoMedioComentarios = totalTamanhoComentario / len(self.avaliacoes)
        
        #return totalTamanhoComentario / len(self.avaliacoes)
    
    def getTotalEstrelas(self):

        estrelas = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }

        for avaliacao in self.avaliacoes:

            # quantidade 1 estrela
            if avaliacao["score"] == 1:
                estrelas[1] += 1
            
            elif avaliacao["score"] == 2:
                estrelas[2] += 1

            elif avaliacao["score"] == 3:
                estrelas[3] += 1

            elif avaliacao["score"] == 4:
                estrelas[4] += 1

            else:
                estrelas[5] += 1
        
        self.estrelas = estrelas

        # return estrelas
    
    def getPalavraMaisFrequente(self, listaComentarios = None, palavrasComuns = 1):

        if listaComentarios is None:
            listaComentarios = [] # nova lista se nao for passada nenhuma
            for avaliacao in self.avaliacoes:
                listaComentarios.extend(avaliacao["content"])

        contador = Counter(listaComentarios)

        self.palavraMaisFrequente = contador.most_common(palavrasComuns)

        # return contador.most_common(palavrasComuns)
    

    # analisando comentários positivos/negativos

    def analiseComentariosPositivosPalavras(self):

        comentariosPositivos = [] # armazena somente os comentarios em dicionarios

        for avaliacao in self.avaliacoes:
            if avaliacao["score"] >= 4:
                comentariosPositivos.extend(avaliacao["content"])
                self.exemploComentariosPositivos = avaliacao["content"]

        return comentariosPositivos  # não apagar, precisa dela pras outras funções
    

    def analiseComentariosNegativosPalavras(self):

        comentariosNegativos = []
    
        for avaliacao in self.avaliacoes:
            if avaliacao["score"] <= 2:
                comentariosNegativos.extend(avaliacao["content"])
                self.exemploComentariosNegativos = avaliacao["content"]

        return comentariosNegativos # nao apagar
    
    def analiseComentariosPositivosElogios(self):

        elogiosEncontrados = []

        for palavra in list(self.analiseComentariosPositivosPalavras()):

            if not str(palavra).isalpha(): # checa se n tem algum numero entre a palavra
                continue

            if self.filtrarElogio(palavra):
                elogiosEncontrados.append(palavra)

        contador = Counter(elogiosEncontrados)

        self.principaisElogios = contador.most_common(3)

        # return contador.most_common(3) # retorna os 3 primeiros elogios encontrados


    def analiseComentariosNegativosCriticas(self):

        criticasEncontradas = []

        for palavra in list(self.analiseComentariosNegativosPalavras()):
            
            if not str(palavra).isalpha():
                continue

            if self.filtrarCritica(palavra):
                criticasEncontradas.append(palavra)

        contador = Counter(criticasEncontradas)

        self.principaisCriticas = contador.most_common(3)

        # return contador.most_common(3)


    
    def colherInformacoesAplicativo(self):
        self.getQuantidadeComentarios()
        self.getComentarioCurto()
        self.getComentarioLongo()
        self.getTamanhoMedioComentarios()
        self.getMediaNotas()
        self.getPalavraMaisFrequente()
        self.getTotalEstrelas()
        self.analiseComentariosPositivosPalavras()
        self.analiseComentariosPositivosElogios()
        self.analiseComentariosNegativosPalavras()
        self.analiseComentariosNegativosCriticas()
