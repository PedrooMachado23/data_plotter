import os

def gerarSaida(ssh, caminho):
    '''Gera uma saida com os conteúdos de um diretório no servidor'''
    
    sftp = ssh.open_sftp()
    saida = sftp.listdir(caminho)

    for index in range(len(saida)):
        arquivo = saida[index]
        metaData = sftp.stat(f'{caminho}/{arquivo}')
        #print metaData
        if 'd' == str(metaData)[0]: #caso seja um dir
            saida[index] += '/'
    return saida