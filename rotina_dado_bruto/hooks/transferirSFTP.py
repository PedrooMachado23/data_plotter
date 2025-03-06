import paramiko

def transferirSFTP(ssh, origem, destino):
    sftp = ssh.open_sftp()
    sftp.get(origem, destino)
    sftp.close()