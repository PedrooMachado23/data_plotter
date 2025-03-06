import os

def apagarDiretorioRecursivo(caminhoRaiz):
    '''Apaga recursivamente uma pasta por inteiro'''
    conteudo = os.listdir(caminhoRaiz)

    for subItem in conteudo:
        caminhoItem = os.path.join(caminhoRaiz, subItem)

        if os.path.isdir(caminhoItem):
            apagarDiretorioRecursivo(caminhoItem)
            continue
        os.remove(caminhoItem) #apaga o arquivo
    os.rmdir(caminhoRaiz) #apaga a pasta