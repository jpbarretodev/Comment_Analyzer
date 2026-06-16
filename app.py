from google_play_scraper import Sort, reviews
from config import Config
from utils import Utils
from collections import Counter
from front import exibir_painel_geral

# Recolhendo os dados da API (Apenas os 3 aplicativos ativos)
whatsApp = reviews(
    "com.whatsapp",
    "pt",
    "br",
    Sort.NEWEST,
    500
)

instagram = reviews(
    "com.instagram.android",
    "pt",
    "br",
    Sort.NEWEST,
    500
)

spotify = reviews (
    "com.spotify.music",
    "pt",
    "br",
    Sort.NEWEST,
    500
)

nomeApps = ["WhatsApp", "Instagram", "Spotify"]

contador = 0 # fiz isso aqui por preguiça, realmente

# limpando as chaves desnecessarias e mantendo os dados originais e guardando numa lista
appsChavesBasicas = {}
for appApiDatas in [whatsApp, instagram, spotify]:
    appsChavesBasicas[nomeApps[contador]] = Config.tratarDadosBrutos(appApiDatas[0])
    contador += 1


# Filtrando os dados da API
configWhatsApp = Config(list(whatsApp)[0])
configInstagram = Config(list(instagram)[0])
configSpotify = Config(list(spotify)[0])


# Gerando os objetos configurados
appWhatsApp = Utils(configWhatsApp.limparComentario())
appInstagram = Utils(configInstagram.limparComentario())
appSpotify = Utils(configSpotify.limparComentario())

# bindando os apps filtrados
for app in [appWhatsApp, appInstagram, appSpotify]:
	app.colherInformacoesAplicativo() # todos os aplicativos já estando com os dados recolhidos prontos para uso
      
#criando a função de escrever
def escreverArquivo(descricoes: dict, nomeApp: str):
            with open (f"avaliacoesOriginais/{nomeApp}", "w", encoding="utf-8") as file:
                for descriptionApp in descricoes:
                    file.write(f"{descriptionApp}\n\n")

# gerando os arquivos .txt
for app in nomeApps:
      escreverArquivo(appsChavesBasicas[app], f"{app}.txt")


# recolhendo os dados finais de comparação
def maiorAvaliacao(appsConfigurados: list):
    appMaiorAvaliacao = {
          "nomeApp": "",
          "mediaNota": 0
    }

    for app in appsConfigurados:
          if app["score"] > appMaiorAvaliacao["mediaNota"]:
                appMaiorAvaliacao["nomeApp"] = app["nomeApp"]
                appMaiorAvaliacao["mediaNota"] = app["score"]

    return appMaiorAvaliacao

def menorAvaliacao(appsConfigurados: list):
      
    appMenorAvaliacao = {
        "nomeApp": appsConfigurados[0]["nomeApp"],
        "mediaNota": appsConfigurados[0]["score"]
      }

    for app in appsConfigurados[1:]:
            if app["score"] < appMenorAvaliacao["mediaNota"]:
                  appMenorAvaliacao["nomeApp"] = app["nomeApp"]
                  appMenorAvaliacao["mediaNota"] = app["score"]

    return appMenorAvaliacao

def principaisProblemas(appsConfigurados: list):
    criticas = []

    for critica in appsConfigurados:
        criticas.extend(critica)

    return Counter(criticas).most_common(3)    

def principaisElogios(appsConfigurados: list):
    elogios = []

    for elogio in appsConfigurados:
        elogios.extend(elogio)

    return Counter(elogios).most_common(3)


# preparação da chamada do front (Front feito pela IA)

# --- MONTA O DICIONÁRIO DE CONFIGURAÇÃO ---
aplicativos = {
    "WhatsApp": appWhatsApp,
    "Instagram": appInstagram,
    "Spotify": appSpotify
}

# --- CHAMA O PAINEL DE FORMA LIMPA ---
exibir_painel_geral(
    aplicativos=aplicativos, 
    nomeApps=nomeApps, 
    maiorAvaliacao=maiorAvaliacao, 
    menorAvaliacao=menorAvaliacao, 
    principaisProblemas=principaisProblemas, 
    principaisElogios=principaisElogios,
    appsChavesBasicas=appsChavesBasicas
)
