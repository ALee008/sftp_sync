import paramiko

remote_ip = 'test.rebex.net'
remote_port = 22
user = "demo"
password = "password"
download_path = "./data/imap-console-client.png"
remote_path = "./pub/example/imap-console-client.png"

# create sftp object
transport = paramiko.Transport((remote_ip, remote_port))
transport.connect(username=user, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.get(remote_path, download_path)
transport.close()