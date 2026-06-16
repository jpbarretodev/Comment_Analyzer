from collections import Counter
import nltk
from nltk.stem.rslp import RSLPStemmer


class KeyWords:

    def __init__(self):

        try:
            self.stemmer = RSLPStemmer()
        except LookupError:
            nltk.download("rslp")
            self.stemmer = RSLPStemmer()


        elogios_base = [
            "bom",
            "lindo",
            "ótimo",
            "maravilhoso",
            "excelente",
            "perfeito",
            "amei",
            "recomendo",
            "adorou",
            "parabéns",
            "rápido",
            "sucesso",
        ]
        criticas_base = [
            "ruim",
            "péssimo",
            "horrível",
            "quebrou",
            "atrasou",
            "defeito",
            "lento",
            "pobre",
            "odiei",
            "errado",
            "falhou",
            "pior",
        ]

        ###
        # essas coisas aqui fazem as palavras serem cortadas na ultima letra, podendo ser
        # avaliadas em todos os generos (masc, fem). Importante ter aqui pra estudar depois
        # ###
        self.raizes_elogios = {self.stemmer.stem(palavra.lower()) for palavra in elogios_base}
        self.raizes_criticas = {self.stemmer.stem(palavra.lower()) for palavra in criticas_base}


    def filtrarElogio(self, palavra): # retorna true se for elogio
        raiz = self.stemmer.stem(str(palavra).strip().lower())
        return raiz in self.raizes_elogios
        

    def filtrarCritica(self, palavra): # retorna true se for critica
        raiz = self.stemmer.stem(str(palavra).strip().lower())
        return raiz in self.raizes_criticas