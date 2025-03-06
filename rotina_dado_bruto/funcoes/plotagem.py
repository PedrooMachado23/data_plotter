#TODO: ideia para resolver o problema das pastas: fazer um dict que tenha uma lista de plots(lista) e usar o nome da subpasta como sendo a chave.
import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plots = {}

def plotagem(caminhos):
    def sensores():
        sensores = []
        for caminhoArquivo in caminhos:
            referencia = caminhoArquivo.rfind('\\')
            sensor = caminhoArquivo[referencia+1:]
            subpasta = caminhoArquivo[:referencia]
            if sensor not in sensores:
                sensores.append(sensor)
            if subpasta not in plots:
                plots[subpasta] = []
        return len(sensores)
    
    global plots
    quantidadeSensores = sensores()
    totalArquivos = quantidadeArquivos = len(caminhos)

    for arquivo in caminhos:
        montarDataframe(arquivo)

    for subpasta in plots:
        labels = plots[subpasta][0]
        data = labels[5]
        analise = re.search(r'[a-zA-Z]+',labels[6])

        if len(plots[subpasta]) <= 3:
            fig, ax = plt.subplots(1,3)
            # fig.suptitle(f'Pasta: {subpasta[subpasta.rfind('\\')+1:]}. {analise.group()} {data[:-3]}', fontsize=30)
            for coluna in range(3):
                try:
                    listaDados = plots[subpasta][coluna]
                    uniX = listaDados[0]
                    match = re.search(r'\w+\s([\w\s\W]+$)', listaDados[1])
                    uniY = f'{match.group(1)}'
                    equipamento = listaDados[2]
                    eixoX = listaDados[3]
                    eixoY = listaDados[4]
                except:
                    continue
                ax[coluna].plot(eixoX, eixoY, color='black')
                ax[coluna].set_title(f'N = {eixoY.shape[1]}', fontsize=15)
                ax[coluna].set_ylabel(f'{equipamento} {uniY}', fontsize=15)
                ax[coluna].set_xlabel(f'{uniX}', fontsize=15)
                ax[coluna].set_xticks((np.arange(eixoX[0], 910, 150)))
        else:
            fig, ax = plt.subplots(2,3)
            # fig.suptitle(f'Pasta: {subpasta[subpasta.rfind('\\')+1:]}. {analise.group()} {data[:-3]}', fontsize=30)
            for linha in range(2):
                for coluna in range(3):
                    try:
                        listaDados = plots[subpasta][linha*3+coluna]
                        uniX = listaDados[0]
                        match = re.search(r'\w+\s([\w\s\W]+$)', listaDados[1])
                        uniY = f'{match.group(1)}'
                        equipamento = listaDados[2]
                        eixoX = listaDados[3]
                        eixoY = listaDados[4]
                    except:
                        continue

                    ax[linha, coluna].plot(eixoX, eixoY, color='black')
                    ax[linha, coluna].set_title(f'N = {eixoY.shape[1]}', fontsize=15)
                    ax[linha, coluna].set_ylabel(f'{equipamento} {uniY}', fontsize=15)
                    ax[linha, coluna].set_xlabel(f'{uniX}', fontsize=15)
                    ax[linha, coluna].set_xticks((np.arange(eixoX[0], 910, 150)))
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.tight_layout()
        plt.show()
    plots.clear()


def montarDataframe(arquivo):
    global plots
    dados = [] #[unix, uniy, equipamento, arrx, arry, data, analise]

    dataframe = pd.read_csv(arquivo, delimiter='\t', decimal=',', index_col=0)
    coluna0 = dataframe.columns[0]

    for i in range(2):
        unidade = dataframe.loc[f'Unit{i + 1}', coluna0]
        unidade = unidade[unidade.find(' ', unidade.find(' ')+1)+1:]
        dados.append(unidade)
    
    equipamento = dataframe.loc['IDDevice', coluna0].upper()
    dados.append(equipamento)

    nomeLinhas = dataframe.index.tolist()
    limiteInferior = nomeLinhas.index('[Data]')
    limiteSuperior = nomeLinhas.index('[END] of [Data]')

    dadosBrutos = dataframe.iloc[limiteInferior+1 : limiteSuperior, :]
    quantidadeLinhas = dadosBrutos.shape[0]
    quantidadeColunas = dadosBrutos.shape[1]

    arrx = []
    for index in dadosBrutos.index.to_list():
        arrx.append(float(index))
    arrx = np.round(arrx).astype(int)
    dados.append(arrx)

    arry = np.zeros((quantidadeLinhas, quantidadeColunas))
    for index in range(quantidadeColunas):
        arry[:, index] = dadosBrutos.iloc[:, index]
    dados.append(arry)

    data = dataframe.loc['DateTime', coluna0][:10]
    dados.append(data)

    analise = dataframe.loc['Comment', coluna0].upper()
    dados.append(analise)

    plots[arquivo[:arquivo.rfind('\\')]].append(dados)