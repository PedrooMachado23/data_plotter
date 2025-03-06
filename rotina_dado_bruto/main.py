from interfaces.mainframe import janelaPrincipal
from funcoes.conexao import openSsh
import os

#cria a pasta em que os arquivos serão baixados
caminhoLocalRaiz = os.path.join(os.getcwd(), 'arquivos')
os.makedirs(caminhoLocalRaiz, exist_ok=True)

#cria a pasta para arquivos auxiliares
caminhoInputs = os.path.join(os.getcwd(), 'inputs')
os.makedirs(caminhoInputs, exist_ok=True)

#deleta o conteudo de uma execução anterior
with open(os.path.join(caminhoInputs, 'arquivosLocais.txt'), 'w'):
    pass

ssh = openSsh() #abre a conexao ssh
stdin, stdout, stderr = ssh.exec_command("mkdir -p /home/temp") #cria pasta temporaria para extracao dos arquivos

#inicializa a interface
janelaPrincipal(ssh, caminhoLocalRaiz, caminhoInputs)  