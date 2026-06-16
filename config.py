# configuração da coleta de dados da api
import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True) # faz o download da lista

class Config:

    chaves = [
        "reviewId",
        "userImage",
        "thumbsUpCount",
        "reviewCreatedVersion",
        "replyContent",
        "repliedAt",
        "appVersion"
    ]

    def __init__(self, resultadoQuery: list):
        self.objetoTrabalho = resultadoQuery

    # metodo estatico para tratar dados brutos
    @staticmethod
    def tratarDadosBrutos(resultadoApi):

        chaves_para_deletar = [
            "reviewId",
            "userImage",
            "thumbsUpCount",        
            "reviewCreatedVersion", 
            "replyContent",         
            "repliedAt",
            "appVersion"
        ]
         
        dadosTratados = []

        for dicionario in resultadoApi: 

            copyDicio = dicionario.copy() # copia para nao interferir no principal
            
            # apagando as chaves que sao irrelevantes
            for chave in list(copyDicio.keys()):
                if chave in chaves_para_deletar:
                    del copyDicio[chave]
            
            # traduzindo as chaves que sobraram
            copyDicio["usuario"] = copyDicio.pop("userName")
            copyDicio["comentario"] = copyDicio.pop("content")
            copyDicio["avaliacao/estrela"] = copyDicio.pop("score")
            copyDicio["dataAvaliacao"] = copyDicio.pop("at").strftime("%d/%m/%Y")
                
            dadosTratados.append(copyDicio)

        return dadosTratados 
    
    # entrando no dicionário e apagando as coisas desnecessárias
    def apagarChavesDesnecessaria(self):
        for dicionario in self.objetoTrabalho:
            for chave in list(dicionario.keys()):
                if chave in self.chaves:
                    del dicionario[chave]
    
    def converterDatas(self):
        for dicionario in self.objetoTrabalho:
            dicionario["at"] = dicionario["at"].strftime("%d/%m/%Y")

    def removerUrls(self):
        padrao_url = r"https?://\S+|www\.\S+"
        for dicionario in self.objetoTrabalho:
            texto = str(dicionario["content"])
            dicionario["content"] = re.sub(padrao_url, "", texto)

    def eliminarEmojis(self):
        padrao_emojis = r"[\U00010000-\U0010ffff]"
        for dicionario in self.objetoTrabalho:
            texto_original = str(dicionario["content"])
            texto_limpo = re.sub(padrao_emojis, "", texto_original)
            dicionario["content"] = texto_limpo.strip()

    def removerCaracteresEspeciais(self):
        padrao_especiais = r"[^\w\s]"
        for dicionario in self.objetoTrabalho:
            texto = str(dicionario["content"])
            dicionario["content"] = re.sub(padrao_especiais, "", texto)

    def removerStopWords(self):
        listaStopWords = set(stopwords.words("portuguese"))
        for dicionario in self.objetoTrabalho:
            texto = str(dicionario["content"]).lower() # deixando minusculo pra lib pegar
            palavras = texto.split()
            palavrasLimpas = [p for p in palavras if p not in listaStopWords]
            dicionario["content"] = " ".join(palavrasLimpas)

    def separarPalavras(self):
        for dicionario in self.objetoTrabalho:
            dicionario["content"] = str(dicionario["content"]).split()

    def limparComentario(self):
        self.apagarChavesDesnecessaria()
        self.converterDatas()
        
        # limpeza dos textos
        self.removerUrls()
        self.eliminarEmojis()
        self.removerCaracteresEspeciais()
        self.removerStopWords()
        self.separarPalavras()


        # elimando os comentarios vazios = []
        comentariosValidados = [dicionario for dicionario in self.objetoTrabalho if len(dicionario["content"]) > 0]
        
        return comentariosValidados
