import os

def exibir_painel_geral(aplicativos: dict, nomeApps: list, maiorAvaliacao, menorAvaliacao, principaisProblemas, principaisElogios, appsChavesBasicas):
    """
    Painel visual que consome os dados tratados pela classe Utils e calcula os totais gerais do sistema.
    """
    pasta_arquivos = "avaliacoesOriginais"

    # --- ATUALIZA OS DADOS EXECUTANDO OS MÉTODOS DE CADA APP ---
    for app in aplicativos.values():
        app.analiseComentariosPositivosPalavras()
        app.analiseComentariosNegativosPalavras()

    # --- CÁLCULO DOS TOTAIS GERAIS DO SISTEMA ---
    total_comentarios = 0
    soma_notas = 0
    total_positivos = 0
    total_negativos = 0
    qtd_apps = len(aplicativos)

    for app in aplicativos.values():
        # 1. Soma a quantidade de comentários de cada app
        total_comentarios += app.quantidadeComentarios
        
        # 2. Guarda a nota média para fazer a média geral depois
        soma_notas += app.mediaNotas
        
        # 3. Conta quantos comentários positivos (baseado na sua distribuição de estrelas >= 4)
        total_positivos += sum(app.estrelas.get(nota, 0) for nota in app.estrelas if nota >= 4)
        
        # 4. Conta quantos comentários negativos (baseado na sua distribuição de estrelas <= 2)
        total_negativos += sum(app.estrelas.get(nota, 0) for nota in app.estrelas if nota <= 2)

    # Faz o cálculo final da média global dos apps analisados
    media_geral_avaliacoes = soma_notas / qtd_apps if qtd_apps > 0 else 0


    # --- PREPARANDO OS DADOS PARA AS SUAS FUNÇÕES GLOBAIS ---
    appWhatsApp = aplicativos.get("WhatsApp")
    appInstagram = aplicativos.get("Instagram")
    appSpotify = aplicativos.get("Spotify")

    dados_para_funcoes = [
        {"nomeApp": "WhatsApp", "score": appWhatsApp.mediaNotas, "criticas": appWhatsApp.principaisCriticas, "elogios": appWhatsApp.principaisElogios},
        {"nomeApp": "Instagram", "score": appInstagram.mediaNotas, "criticas": appInstagram.principaisCriticas, "elogios": appInstagram.principaisElogios},
        {"nomeApp": "Spotify", "score": appSpotify.mediaNotas, "criticas": appSpotify.principaisCriticas, "elogios": appSpotify.principaisElogios} 
    ]

    dados_notas = [{"nomeApp": d["nomeApp"], "score": d["score"]} for d in dados_para_funcoes]
    dados_criticas = [d["criticas"] for d in dados_para_funcoes if d["criticas"]]
    dados_elogios = [d["elogios"] for d in dados_para_funcoes if d["elogios"]]

    # Chamando as suas funções globais de ranking/destaques
    melhor_app = maiorAvaliacao(dados_notas)
    pior_app = menorAvaliacao(dados_notas)
    top_criticas = principaisProblemas(dados_criticas)
    top_elogios = principaisElogios(dados_elogios)


    # --- EXIBIÇÃO NO TERMINAL ---
    print("\n" + "╔" + "═"*78 + "╗")
    print(f"║{'📊 PAINEL GERAL DE ANÁLISE DE COMENTÁRIOS':^78}║")
    print("╚" + "═"*78 + "╝")

    # 1. TABELA COMPARATIVA
    print(f" 📋 TABELA COMPARATIVA")
    print(" ┌" + "─"*16 + "┬" + "─"*14 + "┬" + "─"*14 + "┬" + "─"*26 + "┐")
    print(f" │ {'Aplicativo':<14} │ {'Qtd Coment.':<12} │ {'Média Notas':<12} │ {'Tam. Médio (Palavras)':<24} │")
    print(" ├" + "─"*16 + "┼" + "─"*14 + "┼" + "─"*14 + "┼" + "─"*26 + "┤")

    for nome, app in aplicativos.items():
        print(f" │ {nome:<14} │ {app.quantidadeComentarios:<12} │ {app.mediaNotas:<12.2f} │ {app.tamanhoMedioComentarios:<24.1f} │")

    print(" └" + "─"*16 + "┴" + "─"*14 + "┴" + "─"*14 + "┴" + "─"*26 + "┘\n")

    # --- SEÇÃO NOVA: RESUMO CONSOLIDADO GLOBAL ---
    print(" 📈 RESUMO CONSOLIDADO (TOTAL GERAL)")
    print(" ┌" + "─"*74 + "┐")
    print(f" │ • Total de Comentários Analisados : {total_comentarios:<37} │")
    print(f" │ • Média Geral das Avaliações      : {media_geral_avaliacoes:<37.2f} │")
    print(f" │ • Quantidade de Coment. Positivos : {total_positivos:<37} │")
    print(f" │ • Quantidade de Coment. Negativos : {total_negativos:<37} │")
    print(" └" + "─"*74 + "┘\n")

    # 2. DETALHAMENTO POR APLICATIVO
    print(" 🔍 DETALHAMENTO POR APLICATIVO\n")

    for nome, app in aplicativos.items():
        print(f" 📱 [ {nome.upper()} ] " + "─"*(68 - len(nome)))
        
        palavra_txt = ", ".join([f"'{p}' ({q}x)" for p, q in app.palavraMaisFrequente]) if app.palavraMaisFrequente else "Nenhuma"
        print(f"   • Palavras mais comuns : {palavra_txt}")
        
        elogios_txt = ", ".join([f"{p} ({q}x)" for p, q in app.principaisElogios]) if app.principaisElogios else "Nenhum"
        criticas_txt = ", ".join([f"{p} ({q}x)" for p, q in app.principaisCriticas]) if app.principaisCriticas else "Nenhuma"
        print(f"   • Principais Elogios   : {elogios_txt}")
        print(f"   • Principais Críticas  : {criticas_txt}")
        
        estrelas_linhas = [f"⭐{est}: {app.estrelas[est]}" for est in sorted(app.estrelas.keys(), reverse=True)]
        print(f"   • Distribuição de Notas: " + " | ".join(estrelas_linhas))
        
        texto_longo = " ".join(app.comentarioLongo) if app.comentarioLongo else "Vazio"
        texto_curto = " ".join(app.comentarioCurto) if app.comentarioCurto else "Vazio"
        print(f"   • Maior Comentário     : \"{texto_longo}\"")
        print(f"   • Menor Comentário     : \"{texto_curto}\"")

        txt_positivo = " ".join(app.exemploComentariosPositivos) if getattr(app, 'exemploComentariosPositivos', None) else "Nenhum"
        txt_negativo = " ".join(app.exemploComentariosNegativos) if getattr(app, 'exemploComentariosNegativos', None) else "Nenhum"
        
        print(f"   • Exemplo Positivo     : \"{txt_positivo}\"")
        print(f"   • Exemplo Negativo     : \"{txt_negativo}\"")
        print()

    # 3. RANKING E DESTAQUES
    print(" 🏆 DESTAQUES E CORRIDAS DOS APPS")
    print(" ┌" + "─"*74 + "┐")
    print(f" │ 🥇 Maior Avaliação Média: {melhor_app['nomeApp']} ({melhor_app['mediaNota']:.2f} pts){' ':30}│")
    print(f" │ 🔻 Menor Avaliação Média: {pior_app['nomeApp']} ({pior_app['mediaNota']:.2f} pts){' ':30}│")
    print(" ├" + "─"*74 + "┤")

    txt_top_elogios = ", ".join([f"'{p}' ({q}x)" for p, q in top_elogios]) if top_elogios else "Nenhum"
    txt_top_criticas = ", ".join([f"'{p}' ({q}x)" for p, q in top_criticas]) if top_criticas else "Nenhum"
    
    print(f" │ 👍 Elogios comuns no sistema: {txt_top_elogios:<42} │")
    print(f" │ ⚠️ Problemas comuns no sistema: {txt_top_criticas:<41} │")
    print(" └" + "─"*74 + "┘\n")

    # 4. AVISO DE SALVAMENTO DOS ARQUIVOS
    print(" 💾 STATUS DO ARMAZENAMENTO")
    print(" ┌" + "─"*74 + "┐")
    print(f" │ Os arquivos de avaliações originais foram salvos na pasta '{pasta_arquivos}/' │")
    for nome in nomeApps:
        print(f" │  ├── 📄 {nome}.txt {'[PRONTO]':>51} │")
    print(" └" + "─"*74 + "┘\n")

    print("═"*80 + "\n")
