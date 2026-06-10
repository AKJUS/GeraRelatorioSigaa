#
# calculanotas.py : Responsável por efetuar os cálculos com as notas dos alunos
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação

import pandas as pd


def media(trimestre, disc):
    mediasDisc = trimestre.loc[1:, disc +'.3'].copy()

    def converte(valor):
        if valor == '-':
            return 0.0
        return float(str(valor).replace(',', '.'))

    return mediasDisc.map(converte)

