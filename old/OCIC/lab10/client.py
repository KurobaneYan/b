import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 53188))
client_sock.sendall(b'https://www.onliner.by')
client_sock.close()
