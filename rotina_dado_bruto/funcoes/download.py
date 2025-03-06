import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from hooks.gerarSaida import gerarSaida
from hooks.transferirSFTP import transferirSFTP
import time
import os

arquivoExiste = False

def download(ssh, subpastas, caminhoZip, menuConfirmacao, root, itemProgresso):
    '''Transfere os arquivos do servidor remoto'''

    def escreverCaminhos():
        '''Escreve o caminho local para o arquivo transferido'''

        pastaInputs = os.path.join(os.getcwd(), 'inputs')
        with open(os.path.join(pastaInputs, 'arquivosLocais.txt'), 'a') as arquivo:
            arquivo.write(f'{caminhoZip}=')
            for caminho in caminhosLocais:
                if caminho == caminhosLocais[-1]:
                    arquivo.write(f'{caminho}\n')
                    break
                arquivo.write(f'{caminho},')

    caminhosRemotos = []
    caminhosLocais = []
    caminhoLocalRaiz = os.path.join(os.getcwd(), 'arquivos')

    pastaLocal = caminhoZip[19:]
    if '/' in pastaLocal:
        pastaLocal = pastaLocal.replace('/', '-')

    for subpasta in subpastas:
        #cria a subpasta localmente
        subpastaLocal = f'{caminhoLocalRaiz}\\{pastaLocal}\\{subpasta}'
        subpastaRemota = f'/home/temp/{subpasta}'
        os.makedirs(subpastaLocal, exist_ok=True)

        saida = gerarSaida(ssh, subpastaRemota) #gera saida com os conteudos do caminho
        for arquivo in saida:
            if arquivo[-1] == '/':
                continue
            
            #monta o caminho do arquivo remoto
            origemArquivo = f'{subpastaRemota}/{arquivo}'
            caminhosRemotos.append(origemArquivo)

            #monta o caminho local para transferência
            destinoArquivo = os.path.join(subpastaLocal, arquivo)
            if '/' in destinoArquivo:
                destinoArquivo = destinoArquivo.replace('/', '\\')
            caminhosLocais.append(destinoArquivo)

    totalArquivos = len(caminhosRemotos)

    escreverCaminhos()

    for index in range(len(caminhosRemotos)):
        if os.path.exists(caminhosLocais[index]):
            print('arquivo ja existente')
            continue
        else:
            transferirSFTP(ssh, caminhosRemotos[index], caminhosLocais[index])
            # stind, stdout, stder = ssh.exec_command(f'rm -rf "{caminhosRemotos[index]}"')
        root.after(0, lambda: menuConfirmacao.item(itemProgresso, values=f'{index+1}/{totalArquivos}')) #atualiza o texto de progresso

    #TODO: DELETAR OS ARQUIVOS DA PASTA TEMPORÁRIA ASSIM QUE TERMINAR DE BAIXAR

def unzip(ssh, menus, caminhoZip, janela, root, listaThreads):
    '''Extrai apenas os arquivos desejados do zip no servidor'''

    menuConfirmacao, menuConteudoZip = menus
    caminhos = []
    subpastas = []

    #faz com que '.txt' sejam selecionados no comeco
    for subItem in menuConteudoZip.get_children(''):
        if 'selecionado' in menuConteudoZip.item(subItem, 'tags'):
            caminhos.append(menuConteudoZip.item(subItem, 'text'))
    
    if len(caminhos) == 0:
        messagebox.showerror('Atenção', f'Selecione ao menos um arquivo para poder baixar.')
        return
    
    janela.destroy()

    try:
        itemProgresso = menuConfirmacao.item(caminhoZip)
        messagebox.showerror('Atenção', f'O arquivo "{caminhoZip}" ja foi baixado. Clique duas vezes no menu abaixo para deletá-lo.')
        return
    except:
        itemProgresso = menuConfirmacao.insert('', 'end', text=caminhoZip, iid=caminhoZip, values=('Começando'))

    quantidadeDeThreads = len(listaThreads)
    if quantidadeDeThreads > 1:
        # print(f'esperando a thread {quantidadeDeThreads-2}')
        menuConfirmacao.item(itemProgresso, values='Esperando')
        listaThreads[quantidadeDeThreads-2].join()
        # print(f'thread {quantidadeDeThreads-2} comecando')

    for caminhoConteudo in caminhos:
        #extrai o arquivo
        # print(caminhoZip, caminhoConteudo)
        stdin, stdout, stderr = ssh.exec_command(f'unzip "{caminhoZip}" "{caminhoConteudo}" -d /home/temp')
        if '.' not in caminhoConteudo:
            messagebox.showwarning('Atenção', f'O arquivo "{caminhoConteudo}" não possui extensão. A extensão ".txt" será adicionada automaticamente.')
            stdin, stdout, stderr = ssh.exec_command(f'mv "/home/temp{caminhoConteudo}" "/home/temp{caminhoConteudo}.txt"')
        time.sleep(0.05) #para que nao ocorra erro de um arquivo não ser extraido
        
        subpasta = caminhoConteudo[:caminhoConteudo.rfind('/')]
        if subpasta in subpastas:
            continue
        subpastas.append(subpasta)

    
    download(ssh, subpastas, caminhoZip, menuConfirmacao, root, itemProgresso) #comeca a transferência de arquivos
    listaThreads.remove(listaThreads[0])