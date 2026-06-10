#
# manipulaarquivos.py : Responsável por abrir os arquivos do Sigaa, bem como gerar as saídas CSV e TXT
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação

import pandas as pd
import os

class ManipuladorArquivos:
    def __init__(self, path: str):
        self.path = path

    def abre_arquivo_html(self):
        arquivos = [f for f in os.listdir(self.path) if f.endswith(".html")]

        if (len(arquivos) > 1) or (len(arquivos) == 0) :
            try:
                raise KeyboardInterrupt
            finally:
                print("#"*50)
                print('''
                ATENÇÃO!!!

                Deixe apenas UM arquivo .HTML referente ao conselho na pasta ''', self.path, "\n\n")

                print("#"*50)

        caminho = os.path.join(self.path , arquivos[0])
        df = pd.read_html(caminho)[0]
        df = df.rename(columns={"Unnamed: 1_level_0": 'NOME'})
        self.geraArquivoCSV(df, caminho[:-4] + "csv" )

        

    def geraArquivoCSV(self, df, caminho):
        #apaga arquivos .csv que estejam na pasta
        arquivos = [_ for _ in os.listdir(self.path) if _.endswith(".csv")]
        for csv in arquivos:
            os.remove(os.path.join(self.path, csv))

        #cria o arquivo csv
        df.to_csv(caminho)

    def abreArquivoCSV(self):
        arquivos = [_ for _ in os.listdir(self.path) if _.endswith(".csv")]

        if (len(arquivos) != 1) :
            raise ValueError(
                f"Esperado exatamente 1 arquivo .HTML em '{self.path}', "
                f"encontrado {len(arquivos)}."
            )

        caminho = os.path.join(self.path, arquivos[0])
        return pd.read_csv(caminho)


    def geraArquivoComNomeDisciplinas(self, ultimoTrimestre, ordenar: bool = True):
        COLUNAS_POR_DISCIPLINA = 4  # N1, R, F, S
        colunas = ultimoTrimestre.iloc[0].index[4:]  # pula as 4 primeiras (matrícula, nome, etc.)
        
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
