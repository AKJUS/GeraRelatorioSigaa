#
# main.py : Uma solução para o problema de geração de relatório de acompanhamento de notas dos alunos
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação
import pandas as pd
from manipulaarquivos import ManipuladorArquivos
import calculanotas as calcNota
import calculafrequencia as calcFreq
import os

if __name__ == '__main__':

    for i in range(1, 4):
        pasta = "ano" + str(i)
        if not os.path.exists(pasta):
            os.mkdir(pasta)

    #ETAPAS
    #1) Gero os relatórios no Sigaa em HTML e salvo nas respectivas pastas referentes ao ano do técnico: ano1, ano2 e ano3
    #   Dá pra usar o Selenium/Python pra fazer isso, mas não fiz.

    print('''Olá! Antes de tudo, lembre-se de salvar o último arquivo de conselho de classe nas respectivas pastas!
    - 1º ano: pasta ano1
    - 2º ano: pasta ano2
    - 3º ano: pasta ano3

    ATENÇÃO! Os arquivos de conselho de classe gerados pelo Sigaa devem ser salvos como HTML.
    ''')
    input("SE ESTIVER TUDO PRONTO, APERTE ENTER!")

    trimestre = int(input("\n\nEm qual trimestre estamos? (1, 2 ou 3)"))

    resposta = input("Trata-se do Técnico Integrado em Informática? (sim ou nao)").upper()
    if resposta in ('SIM', 'S'):
        #1o = 760+160+400, 2o = 760+200+320 e 3o = 720+240+240
        nAulas1o, nAulas2o, nAulas3o = 1320, 1280, 1200
    else:
        nAulas1o = int(input("\t\t 1o ano - qual o número de aulas? "))
        nAulas2o = int(input("\t\t 2o ano - qual o número de aulas? "))
        nAulas3o = int(input("\t\t 3o ano - qual o número de aulas? "))
    limiarReprovFreq = calcFreq.calculaLimiarPerigoReprovacaoFreq(nAulas1o, nAulas2o, nAulas3o, trimestre)

    print(limiarReprovFreq)


    for ano in range(1, 4):
        #2) Altero a variável 'path' para dizer qual a pasta eu quero que a análise seja feita
        man = ManipuladorArquivos(f"ano{ano}/")
        
        #3) Gerará o CSV destes arquivos HTML
        man.abre_arquivo_html()
        df = man.abreArquivoCSV()

        listaFreqTodosAlunos = calcFreq.somaFaltas(df, limiarReprovFreq[ano-1], trimestre)

        #Gera arquivo na pasta com os nomes das disciplinas daquele ano
        man.geraArquivoComNomeDisciplinas(df,ordenar = False)

        #5) Lê os nomes das disciplinas daquele ano
        disciplinas = man.todasDisciplinas()

        arqSaida = df.loc[1:,'NOME'] #nomes alunos

        #Inicio a junção dos arquivos CSVs para cada disciplina
        for disc in disciplinas:
            disc = disc.strip() #Retirei o '\n' da 1ª disciplina
            arqAux = calcNota.media(df, disc)
            arqSaida = pd.concat([arqSaida,arqAux],axis=1 )
            arqSaida = arqSaida.rename(columns={ disc +'.3': disc})

        arqSaida = pd.concat([arqSaida, listaFreqTodosAlunos], axis=1)

        man.geraSaida(arqSaida, "somaDasFaltasEMedias.csv")


        print("Arquivos gerados! Confira nas pastas.")
