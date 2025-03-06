from tkinter import *
from tkinter import ttk, messagebox
from funcoes.plotagem import plotagem
import os

def janelaPlot(root, caminhoInputs):
    def fecharJanela():
        novaJanela.destroy()
        botaoPlotagem.configure(state='normal')

    def concluirArquivo(chave):
        for subItem in menuConfirmacao.get_children():
            if menuConfirmacao.item(subItem, 'text') == chave:
                menuConfirmacao.item(subItem, tags=('plotado'))

    arquivos = {}
    caminhoArquivostxt = os.path.join(caminhoInputs, 'arquivosLocais.txt')
    botaoPlotagem = root.nametowidget('botaoPlotagem')
    menuConfirmacao = root.nametowidget('frameArquivos').nametowidget('menuConfirmacao')

    with open(os.path.join(caminhoArquivostxt), 'r') as arquivo:
        if os.path.getsize(caminhoArquivostxt) < 1:
            messagebox.showerror('Erro ao preparar arquivos!','Nenhum arquivo foi baixado.')
            return
        for linha in arquivo:
            referencia = linha.find('=')
            zipBaixado = linha[:referencia]
            txts = linha[referencia+1:-1].split(',')
            arquivos[zipBaixado] = txts

    botaoPlotagem.configure(state='disabled')

    novaJanela = Toplevel(root)
    novaJanela.grid()
    novaJanela.protocol('WM_DELETE_WINDOW', lambda: fecharJanela())
    novaJanela.focus_force()
    novaJanela.grab_set()
    
    novaJanelaFrame = ttk.Frame(novaJanela)
    novaJanelaFrame.grid()

    chaves = list(arquivos.keys())
    for index in range(len(arquivos)):
        texto = ttk.Label(novaJanelaFrame, text=f'Arquivo {index}: {chaves[index]}')
        texto.grid(column=0, row=index)

        botaoPlot = ttk.Button(novaJanelaFrame, text='Plotar', command=lambda chave=chaves[index]: [concluirArquivo(chave), plotagem(arquivos[chave])])
        botaoPlot.grid(column=1, row=index)