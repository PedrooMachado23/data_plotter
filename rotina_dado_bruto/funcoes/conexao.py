import paramiko
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def openSsh():
    '''Função que inicia a conexão ssh'''

    ip = getenv('VPN_IP')
    usuario = getenv('SSH_USER')
    senha = getenv('SSH_PASSWD')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username=usuario, password=senha)

    return ssh

def close(ssh):
    '''Função que fecha a conexão'''
    ssh.close()