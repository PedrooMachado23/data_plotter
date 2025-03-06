from tkinter import ttk
from tkinter import *
import threading as th
from funcoes.download import unzip

#TODO: COLOCAR O CAMINHO DOS ARQUIVOS EM UM TXT AUXILIAR

listaThreads = []

def janelaZip(ssh, root):
    '''Cria a janela que contem o conteudo do arquivo .zip selecionado'''

    def carregarConteudo():
        '''Insere os itens no menu de conteudo zip'''
        
        stdin, stdout, stderr = ssh.exec_command(f'unzip -l {caminhoZip}') #lista o conteudo do arquivo zip no terminal
        saida = stdout.read().decode('utf-8').split('\n')
        # print(saida)
        
        for linha in saida[3:-3]:
            # print(linha)
            if linha[-1] == '/':
                continue

            referencia = linha.find('-') #referencia para poder cortar a string
            tamanho = int(linha[:referencia-6])//1024
            data = linha[referencia-4:referencia+6]
            nome = linha[referencia+15:]

            tag = ''
            if '.txt' in linha:
                tag = 'selecionado'
            menuConteudoZip.insert('', 'end', text=nome, values=(data, f'{tamanho} KB'), tags=tag)

    def selecao():
        '''Permite selecionar/deselecionar arquivos'''
        
        if not menuConteudoZip.selection():
            return
        for item in menuConteudoZip.selection():
            itemClicado = menuConteudoZip.selection()[0]
            menuConteudoZip.selection_remove(itemClicado)

            if 'selecionado' in menuConteudoZip.item(itemClicado)['tags']:
                menuConteudoZip.item(itemClicado, tags=())
            else:
                menuConteudoZip.item(itemClicado, tags='selecionado')

    def comecarThread():
        unzipThread = th.Thread(target=unzip, args=(ssh, (menuConfirmacao, menuConteudoZip), caminhoZip, novaJanela, root, listaThreads))
        listaThreads.append(unzipThread)
        unzipThread.start()

    menuArquivos, menuConfirmacao = (root.nametowidget('frameArquivos').nametowidget('menuArquivos'), root.nametowidget('frameArquivos').nametowidget('menuConfirmacao'))
    itemClicado = menuArquivos.selection()[0]

    if '->file'not in itemClicado: #verifica se é um arquivo
        return
    
    caminhoZip = itemClicado[:-6]

    #nova janela criada
    novaJanela = Toplevel(root)
    novaJanela.title('Seleção dos arquivos')
    novaJanela.focus_force()
    novaJanela.grab_set()

    #menu que mostra todo o conteudo do zip
    menuConteudoZip = ttk.Treeview(novaJanela)
    menuConteudoZip['columns'] = ('#1, #2')
    for id, nome in enumerate(('Nome', 'Última modif.', 'Tamanho')):
        menuConteudoZip.heading(f'#{id}', text=nome)
    for id, centralizacao in enumerate(('w', 'e', 'e')):
        menuConteudoZip.column(f'#{id}', anchor=centralizacao)
    for id, largura in enumerate(('410', '90', '75')):
        menuConteudoZip.column(f'#{id}', width=largura)
    menuConteudoZip.bind('<Double-1>', lambda e: selecao())
    menuConteudoZip.grid(column=0, row=0, columnspan=2, padx=(10,0), pady=10)
    menuConteudoZip.tag_configure('selecionado', foreground='white', background='green') #tag que identifica qual item foi clicado

    #scroll para o menu
    menuConteudoZipScroll = ttk.Scrollbar(novaJanela, orient='vertical', command=menuConteudoZip.yview)
    menuConteudoZip['yscrollcommand'] = menuConteudoZipScroll.set
    menuConteudoZipScroll.grid(column=2, row=0, padx=(0,10), pady=10, sticky=((N,S)))

    #botao para começar a extracao dos dados
    botaoConfirmar = ttk.Button(novaJanela, text='Confirmar', command=lambda: comecarThread())
    botaoConfirmar.grid(column=0, row=1, padx=(10,0), pady=(0,10))

    #botao para cancelar a operacao
    botaoCancelar = ttk.Button(novaJanela, text='Cancelar', command=lambda: novaJanela.destroy())
    botaoCancelar.grid(column=1, row=1, padx=(0,10), pady=(0,10))

    carregarConteudo()