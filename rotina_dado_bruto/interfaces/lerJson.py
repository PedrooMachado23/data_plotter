from tkinter import ttk
from tkinter import *

def janelaJson(ssh, root):
    menuArquivos = root.nametowidget('frameArquivos').nametowidget('menuArquivos')

    if not menuArquivos.selection():
        return
    
    itemClicado = menuArquivos.selection()[0][:-6]
    stdin, stdout, stderr = ssh.exec_command(f'cat "{itemClicado}"')
    texto = stdout.read().decode('utf-8')
    print(texto)

    novaJanela = Toplevel(root)
    novaJanela.title('Leitura JSON')
    novaJanela.focus_force()
    novaJanela.grab_set()

    fonte = root.option_get('Text', 'font')

    areaTexto = Text(novaJanela, width=40, height=25, wrap='word')
    areaTexto.grid(column=0, row=0, padx=10, pady=10)
    areaTexto.insert(INSERT, texto)
    areaTexto.config(state='disabled')

    areaTextoScroll = ttk.Scrollbar(novaJanela, orient='vertical', command=areaTexto.yview)
    areaTexto['yscrollcommand'] = areaTextoScroll.set
    areaTextoScroll.grid(column=1, row=0, sticky=((N,S)), padx=(0,10))
    