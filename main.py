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
    #1) Pega as informações gerais do curso
    man = ManipuladorArquivos("ano1/")
    man.abre_arquivo_html()
    matriz = man.geraAmbiente()

    for ano in range(1, 4):
        #2) Altero a variável 'path' para dizer qual a pasta eu quero que a análise seja feita
        man = ManipuladorArquivos(f"ano{ano}/")
        
        #3) Gerará o CSV destes arquivos HTML
        man.abre_arquivo_html()
        df = man.abreArquivoCSV()

        listaFreqTodosAlunos = calcFreq.somaFaltas(df, matriz['limiarRepr'][str(ano)], matriz['trimestre'])

        #Gera arquivo na pasta com os nomes das disciplinas daquele ano
        man.geraArquivoComNomeDisciplinas(df,ordenar = False)

        #5) Lê os nomes das disciplinas daquele ano
        disciplinas = man.todasDisciplinas()
        

        arqSaida = df.loc[1:,'NOMES'] #nomes alunos
        
        #Inicio a junção dos arquivos CSVs para cada disciplina
        for disc in disciplinas:
            disc = disc.strip() #Retirei o '\n' da 1ª disciplina
            arqAux = calcNota.media(df, disc)
            arqSaida = pd.concat([arqSaida,arqAux],axis=1 )
            arqSaida = arqSaida.rename(columns={ disc +'.3': disc})

        arqSaida = pd.concat([arqSaida, listaFreqTodosAlunos], axis=1)

        man.geraSaida(arqSaida, "somaDasFaltasEMedias.csv")


        print("Arquivos gerados! Confira nas pastas.")
        
