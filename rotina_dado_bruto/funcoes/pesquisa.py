from hooks.gerarSaida import gerarSaida

def pesquisar(ssh, frame):
    '''Coloca os itens do servidor remoto no menu'''
    menu = frame.nametowidget('menuArquivos')
    #caso não consiga, significa que é execucao de quando o programa é iniciado (nenhum item foi clicado)
    try:
        caminho = itemClicado = menu.selection()[0]
        if not menu.selection(): #impede a funcao de repetir
            return
        if len(menu.get_children(itemClicado)) > 1 or '->file' in itemClicado:
            return
        
        #deleta o item fantasma do menu
        for subItem in menu.get_children(itemClicado):
            menu.delete(subItem)
    except:
        caminho = '/home/archive/data/'
        itemClicado = ''
    
    saida = gerarSaida(ssh, caminho) #gera conteudo do diretório
    
    for item in saida:
        diretorio = False
        if item[-1] == '/':
            diretorio = True

        novoCaminho = f'{caminho}{item}'
        # print(novoCaminho)
        itemMenu =  menu.insert(itemClicado, 'end', text=f'  {item[:-1]}', iid=novoCaminho)
        menu.insert(itemMenu, 'end', text='', iid=f'{novoCaminho}_') #item fantasma para mostrar checkbox
        if diretorio == False:
            menu.delete(itemMenu)
            menu.insert(itemClicado, 'end', text=f'  {item}', iid=f'{novoCaminho}->file')
        menu.item(itemClicado, open=True)