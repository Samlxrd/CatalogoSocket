import socket
import threading
import time
import catalogo

PORT = 5050
HOST = '127.0.0.1'

ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clientes = []

def handle_client(conn, addr):
    try:

        connected = True

        # Recebe nome de usuário do cliente
        name = conn.recv(1024).decode('utf-8')
        clientes.append((conn, name))
        print(f"[!] [+] ({addr}) {name} conectou-se.")


        while connected:
            msg = conn.recv(1024).decode('utf-8')
            if msg:
                print(f'[LOG] ({addr}) {name}: {msg}')

    finally:
        clientes.remove((conn, name))
        print(f'[LOG] Desconectando: ({addr,name})')
        conn.close()

def start():
    server.listen()
    print(f'[!] Servidor ativo [{HOST}]')

    # Inicializa o Banco de Dados do catálogo caso ele não exista
    ctlg = catalogo.Catalogo()

    # Se os tipos não tiverem cadastrados, o cadastro é feito.
    # Tipos: (Filme, Serie, Anime, Outro)
    if not ctlg.query_types():
        ctlg._criar_tipos()

    ctlg.close_connection()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[*] Conexões ativas: {threading.active_count() - 1}")

print("[!] O Servidor está inicializando...")
print("[!] LOG Message format: [LOG] [{NOME}]: {MENSAGEM}")
start()
