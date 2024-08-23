import paramiko
import os
from src.utils.config_loader import load_config
from src.utils.CRemote import CRemote


class Filetransfer():
    '''主要用于文件的上传和下载'''

    def __init__(self, fp=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config/remote.yml").replace("\\","/")):
        self.config = load_config(fp)

    def __enter__(self):
        cremote = CRemote()
        hostname = cremote.hostname
        port = cremote.port
        username = cremote.username
        password = cremote.password
        private_key_path = cremote.private_key_path
        try:
            # 建立SSH客户端
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 使用密码或私钥连接
            if password:
                self.ssh.connect(hostname, port, username, password)
            elif private_key_path:
                key = paramiko.RSAKey.from_private_key_file(private_key_path)
                self.ssh.connect(hostname, port, username, pkey=key)
            else:
                raise ValueError("需要提供密码或私钥路径")

            # 使用SFTP从远程服务器下载文件
            self.sftp = self.ssh.open_sftp()
        except Exception as e:
            raise f"文件下载失败: {e}"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Exception caught: {exc_type}")
        self.sftp.close()
        self.ssh.close()

    def file_exists(self, remote_path):
        try:
            self.sftp.stat(remote_path)  # 尝试获取远程文件的状态
            return True
        except FileNotFoundError:
            return False

    def download_file(self, remote_path, local_path):
            if self.file_exists( remote_path):
                print(f"远程文件 {remote_path} 存在，开始下载...")
                self.sftp.get(remote_path, local_path)
                print(f"文件已成功下载到: {local_path}")
            else:
                print(f"远程文件 {remote_path} 不存在，取消下载操作。")

            self.sftp.get(remote_path, local_path)
            print(f"文件已成功下载到: {local_path}")


