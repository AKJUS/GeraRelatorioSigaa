#
# manipulaarquivos.py : Responsável por abrir os arquivos do Sigaa, bem como gerar as saídas CSV e TXT
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação

import pandas as pd
import os
from bs4 import BeautifulSoup
import calculafrequencia as calcFreq
import re


class ManipuladorArquivos:
    def __init__(self, path: str):
        self.path = path
        self.metadata = {}
        self.info_curso = {}

    def abre_arquivo_html(self):
        arquivos = [f for f in os.listdir(self.path) if f.endswith(".html")]

        if len(arquivos) != 1:
            raise ValueError(
                f"Esperado exatamente 1 arquivo .HTML em '{self.path}', "
                f"encontrado {len(arquivos)}."
            )

        caminho = os.path.join(self.path , arquivos[0])

        # Extrai metadados do cabeçalho
        with open(caminho, encoding='windows-1252') as f:
            soup = BeautifulSoup(f, 'html.parser')

        itens = soup.find_all('div', style=lambda s: s and 'font-weight: bold' in s)
        for item in itens:
            texto = item.text.strip()
            if ':' in texto:
                chave, valor = texto.split(':', 1)
                self.metadata[chave.strip()] = valor.strip()


        df = pd.read_html(caminho, encoding='windows-1252')[0]
        df = df.rename(columns={"Unnamed: 1_level_0": 'NOMES'})
        df = df.rename(columns=lambda col: re.sub(r'^Unnamed:.*', '', col))
        
        self.geraArquivoCSV(df, caminho[:-4] + "csv" )
        #return self.metadata
        

    def geraAmbiente(self):
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

        ano = self.metadata['Módulo'].split()[1]
        trimestre = int(self.metadata['Bimestre/Trimestre'])
        curso = self.metadata['Estrutura Curricular']

        if curso == 'TÉCNICO EM INFORMÁTICA - TIINF05003 (INT) [0320251 - 2025]':
            nAulas1o, nAulas2o, nAulas3o = 1240,1240,1160
        elif curso == 'TÉCNICO EM INFORMÁTICA - TIINF05003 (INT) [0320231 - 2023]':
            #1o = 760+160+400, 2o = 760+200+320 e 3o = 720+240+240
            nAulas1o, nAulas2o, nAulas3o = 1320, 1280, 1200
        else:
            print(f"O curso {curso} não tem o número de aulas por ano cadastrados no sistema\nInforme abaixo:\n")
            nAulas1o = int(input("\t\t 1o ano - qual o número de aulas? "))
            nAulas2o = int(input("\t\t 2o ano - qual o número de aulas? "))
            nAulas3o = int(input("\t\t 3o ano - qual o número de aulas? "))
        limiarReprovFreq = calcFreq.calculaLimiarPerigoReprovacaoFreq(nAulas1o, nAulas2o, nAulas3o, trimestre)


        self.info_curso = {
            'curso': curso,
            'trimestre': trimestre,
            'matriz': {'1':nAulas1o, '2': nAulas2o, '3': nAulas3o},
            'limiarRepr': {'1':limiarReprovFreq[0], '2': limiarReprovFreq[1], '3': limiarReprovFreq[2]}
        }

        return self.info_curso

    def geraArquivoCSV(self, df, caminho):
        #apaga arquivos .csv que estejam na pasta
        arquivos = [_ for _ in os.listdir(self.path) if _.endswith(".csv")]
        for csv in arquivos:
            os.remove(os.path.join(self.path, csv))

        #cria o arquivo csv
        df.to_csv(caminho)

    def abreArquivoCSV(self):
        arquivos = [_ for _ in os.listdir(self.path) if _.endswith(".csv")]

        if len(arquivos) != 1:
            raise ValueError(
                f"Esperado exatamente 1 arquivo .CSV em '{self.path}', "
                f"encontrado {len(arquivos)}."
            )

        caminho = os.path.join(self.path, arquivos[0])
        return pd.read_csv(caminho)


    def geraArquivoComNomeDisciplinas(self, df, ordenar: bool = True):
        COLUNAS_POR_DISCIPLINA = 4  # N1, R, F, S
        colunas = df.iloc[0].index[4:]  # pula as 4 primeiras (matrícula, nome, etc.)
        
        nomes_disciplinas = []
        for i, col in enumerate(colunas):
            # A coluna de nota (N1) é a primeira de cada grupo de 4
            if i % COLUNAS_POR_DISCIPLINA == 0:
                # Remove sufixo de nível como '.1', '.2', '.3'
                nome = col.split('.')[0] if '.' in col else col
                nomes_disciplinas.append(nome)
        
        if ordenar:
            nomes_disciplinas = sorted(nomes_disciplinas)

        with open(os.path.join(self.path, "nomes_disciplinas.txt"), 'w') as file:
            for nome in nomes_disciplinas:
                file.write(nome + "\n")

    def todasDisciplinas(self):
        caminho = os.path.join(self.path, "nomes_disciplinas.txt")
        with open(caminho) as file:
            return [linha.strip() for linha in file.readlines()]

    def geraSaida(self, df, nome_arquivo):
        caminho = os.path.join(self.path, nome_arquivo)
        df.to_csv(caminho)
