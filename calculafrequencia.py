#
# calculanotas.py : Responsável por efetuar os cálculos das frequências dos alunos
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação
import pandas as pd

def somaFaltas(dadosUltimoTrimestre, limiarReprovFreq, trimestre):
    alunos = dadosUltimoTrimestre.shape[0]
    colunas = dadosUltimoTrimestre.shape[1]

    listaFreqTodosAlunos = [["", ""]]
    for i in range(1, alunos):
        linhaAluno = dadosUltimoTrimestre.iloc[i]
        freqAlunoTotal = 0
        for j in range(6, colunas, 4): #Primeira coluna da frequência é a 6, próxima é a 10, ...
            if linhaAluno.iloc[j] != '-':
                freqAlunoTotal+= int(linhaAluno.iloc[j])

        if freqAlunoTotal>= limiarReprovFreq[0]:
            listaFreqTodosAlunos.append([freqAlunoTotal, "Reprovado"])
        elif trimestre != 3 and freqAlunoTotal>= limiarReprovFreq[1]:
            listaFreqTodosAlunos.append([freqAlunoTotal, "Risco"])
        else:
            listaFreqTodosAlunos.append([freqAlunoTotal, "Ok"])

    df = pd.DataFrame (listaFreqTodosAlunos, columns = ['FALTAS', 'REP. FALTAS?'])


    return df

'''
1º ano = 1360 -> 25% = 340 faltas
2º ano = 1280 -> 25% = 320 faltas
3º ano = 1360 -> 25% = 340 faltas
'''

def calculaLimiarPerigoReprovacaoFreq(nAulas1o, nAulas2o, nAulas3o, trimestre):
    limiarRepr1o = round(nAulas1o * 0.25)
    limiarRepr2o = round(nAulas2o * 0.25)
    limiarRepr3o = round(nAulas3o * 0.25)

    limiarCritico1o = round((limiarRepr1o/3)*0.90) * trimestre
    limiarCritico2o = round((limiarRepr2o/3)*0.90) * trimestre
    limiarCritico3o = round((limiarRepr3o/3)*0.90) * trimestre

    return [[limiarRepr1o, limiarCritico1o], [limiarRepr2o, limiarCritico2o], [limiarRepr3o, limiarCritico3o]]
    