from tkinter import ttk, messagebox
from tkinter import *
from funcoes.pesquisa import pesquisar
from hooks.apagarDiretorioRecursivo import apagarDiretorioRecursivo
from interfaces.plots_menu import janelaPlot
from interfaces.zip_content import janelaZip
from interfaces.lerJson import janelaJson
import os



def janelaPrincipal(ssh, caminhoLocalRaiz, caminhoInputs):
    '''Começa o programa''' 

    #TODO: TIRAR A PERGUNTA SOBRE APAGAR ARQUIVOS NA VERSAO FINAL
    def fecharPrograma():
        '''Fecha o programa e apaga os arquivos'''

        resposta = messagebox.askquestion("Confirmação", "Apagar os arquivos baixados?")
        if resposta == 'yes':
            try:
                apagarDiretorioRecursivo(caminhoLocalRaiz) #apaga todos os arquivos baixados
            except:
                pass
        stdin, stdout, stderr = ssh.exec_command('rm -rf /home/temp') #apaga a pasta temporaria criada no servidor
        ssh.close()
        root.destroy()

    def encaminharArquivo():
        funcoes = {'.zip' : [janelaZip, [ssh, root]],
                   '.json' : [janelaJson, [ssh, root]]}
        
        if not menuArquivos.selection():
            return
        
        itemClicado = menuArquivos.selection()[0]
        for item in funcoes:
            if item in itemClicado:
                funcao, argumentos = funcoes[item]
                funcao(*argumentos)

    def apagarArquivoMenuConfirmacao():
        if not menuConfirmacao.selection():
            return
        itemClicado = menuConfirmacao.selection()[0]

        resposta = messagebox.askquestion("Confirmação", f"Apagar o item: {itemClicado}?")
        if resposta == 'no':
            return
        
        menuConfirmacao.delete(itemClicado)

        with open(os.path.join(caminhoInputs, 'arquivosLocais.txt'), 'r') as leitura:
            linhas = leitura.readlines()        
        #TODO: APAGANDO LINHA ERRADA
        with open(os.path.join(caminhoInputs, 'arquivosLocais.txt'), 'w') as arquivo:
            for linha in linhas:
                if itemClicado in linha:
                    arquivo.write(linha)
        
        for pasta in os.listdir(caminhoLocalRaiz):
            if pasta in itemClicado.replace('/','-'):
                apagarDiretorioRecursivo(os.path.join(caminhoLocalRaiz, pasta))


    root = Tk()

    frameArquivos = ttk.Frame(root, name='frameArquivos')
    frameArquivos.grid(column=1, row=0, padx=10)

    #menu com arquivos do servidor
    menuArquivos = ttk.Treeview(frameArquivos, style='Custom.Treeview', name='menuArquivos')
    menuArquivos.heading('#0', text='Campanhas', anchor=W)
    menuArquivos.column('#0', width=500)
    menuArquivos.grid(column=0, row=0)
    menuArquivos.bind('<<TreeviewSelect>>', lambda e: pesquisar(ssh, frameArquivos))
    menuArquivos.bind('<Double-1>', lambda e: encaminharArquivo())

    #scroll para o menuArquivos
    menuArquivosScroll = ttk.Scrollbar(frameArquivos, orient='vertical', command=menuArquivos.yview)
    menuArquivos['yscrollcommand'] = menuArquivosScroll.set
    menuArquivosScroll.grid(column=1, row=0, sticky=((N,S)), padx=(0,10))

    #menu que contem os arquivos ja baixados
    menuConfirmacao = ttk.Treeview(frameArquivos, height=5, name='menuConfirmacao')
    menuConfirmacao['columns'] = ('#1')
    for id, texto in enumerate(('Nome', 'Progresso')):
        menuConfirmacao.heading(f'#{id}', text=texto)
    for id, centralizacao in enumerate(('w', 'e')):
        menuConfirmacao.column(f'#{id}', anchor=centralizacao)
    for id, largura in enumerate(('400', '100')):
        menuConfirmacao.column(f'#{id}', width=largura)
    menuConfirmacao.grid(column=0, row=1, pady=10, padx=10, sticky=((E,W)))
    menuConfirmacao.tag_configure('plotado', foreground='white', background='green')
    menuConfirmacao.bind('<Double-1>', lambda e: apagarArquivoMenuConfirmacao())

    #botao para plotar os dados
    botaoPlotagem = ttk.Button(root, text='Visualizar dados', command=lambda: janelaPlot(root, caminhoInputs), name='botaoPlotagem')
    botaoPlotagem.grid(column=0, row=0, padx=10)
    
    tree_1 = ttk.Style()
    tree_1.configure('Custom.Treeview', indent=10)

    root.protocol("WM_DELETE_WINDOW", lambda: fecharPrograma())

    pesquisar(ssh, frameArquivos)

    #começa a aplicação
    root.mainloop()