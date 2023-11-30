import socket
import catalogo
import threading
import json

class ServerSocket:
    def __init__(self, HOST, PORT):
        
        self.ADDR = (HOST, PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.clients = []

    # Desliga servidor
    def stop_server(self):
        self.server.close()

    # Inicia servidor
    def start_server(self):

        print("[!] O Servidor está inicializando...")
        self.server.listen()
        print(f'[!] Servidor ativo [{self.ADDR[0]}]')
        print(f'[!] Padrão de log para requisições e respostas')
        print(f"[!] [LOG] <username>: <requisição>")
        print(f"[!] [LOG] Response: <response_status>\n")


        # Inicializa o Banco de Dados do catálogo caso ele não exista
        self.ctlg = catalogo.Catalogo()
        self.ctlg._criar_tabelas()

        # Se os tipos não tiverem cadastrados, o cadastro é feito.
        # Tipos: (Filme, Serie, Anime, Outro)
        if not self.ctlg.query_types():
            self.ctlg._criar_tipos()

        self.ctlg.close_connection()

        # Aguarda conexão de um cliente ao servidor
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[*] Conexões ativas: {threading.active_count() - 1}")


    # Função responsável por enviar dados para um cliente.
    def send_data(self, conn, data):
        message = json.dumps(data)
        conn.send(message.encode())


    # Função responsável por receber dados de um cliente.
    def receive_data(self, conn):
        data = conn.recv(1024).decode()
        if data:
            data = json.loads(data)
        return data


    # Tratamento das requisições e respostas Cliente x Servidor
    def handle_client(self, conn, addr):
        client_username = ''
        try:
            connected = True

            # Rececbe o nome de usuário do cliente conectado.
            data = self.receive_data(conn)
            client_username = data['username']
            self.clients.append((conn, client_username))

            # Se for a primeira vez que esse nome de usuário
            # é conectado, ele é adicionado ao banco de dados.
            db = catalogo.Catalogo()
            try:
                user = db.get_user_id(client_username)

                if not user:
                    try:
                        query = db.insert_user(client_username)
                        print('Usuário cadastrado: ', client_username)
                    
                    except:
                        print('Falha ao cadastrar usuario: ', client_username)

            except:
                print('Falha ao buscar cadastro.')

            db.close_connection()
            
            print(f"[!] [+] ({addr}) {client_username} conectou-se ao servidor.\n")

            while connected:

                # Recebe uma ação do cliente (requisição)
                data = self.receive_data(conn)
                if not data:
                    break
                
                # Conecta ao banco de dados
                db = catalogo.Catalogo()
                print(f'[LOG] ({addr}, {client_username}) : {data}')

                # Requisição 'query_all': retorna todos os itens cadastrados no catálogo
                if data['action'] == 'query_all':
                    try:
                        query = db.query_items()

                        response = {"status": "OK", "data":[]}
                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})

                    except:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)

                
                # Requisição 'query_favorites': retorna todos os itens favoritados do usuário.
                elif data['action'] == 'query_favorites':
                    try:
                        query = db.query_favorites(data['user_id'])

                        response = {"status": "OK", "data":[]}
                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})
                    
                    except:
                        response = {"status": "ERROR"}
                    
                    self.send_data(conn, response)


                # Requisição 'insert_item': registra item no catálogo.
                elif data['action'] == 'insert_item':
                    try:
                        # Verifica se o item ja foi cadastrado
                        query = db.was_registered(data['item_name'], data['item_type'])

                        if not query:
                            try:
                                query = db.insert_item(data['item_name'], data['item_type'])
                                response = {"status": "OK"}
                            
                            except:
                                response = {"status": "ERROR"}
                        
                        else:
                            response = {"status": "ERROR"}

                    except:
                        print('alooo')
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)

                
                # Requisição 'insert_favorite': Registra item nos favoritos do usuário.
                elif data['action'] == 'insert_favorite':
                    try:
                        # Verifica se o item ja foi cadastrado
                        query = db.was_favorited(data['user_id'], data['item_id'])

                        if not query:
                            try:
                                query = db.insert_favorites(data['user_id'], data['item_id'])
                                response = {"status": "OK"}

                            except:
                                response = {"status": "ERROR"}

                        else: response = {"status": "ERROR"}

                    except:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)
                

                # Requisição 'get_user_id': retorna id do usuário
                elif data['action'] == 'get_userid':
                    try:
                        query = db.get_user_id(data['user_name'])
                        response = {"status": "OK", "data":[]}

                        for x in query:
                            response['data'].append({'user_id': x[0]})
                        
                    except:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)
                

                # Requisição 'search_item': busca no catálogo e retorna os itens encontrados.
                elif data['action'] == 'search_item':
                    try:
                        query = db.search_items(data['item_name'])
                        response = {"status": "OK", "data":[]}

                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})
                    
                    except:
                        response = {"status": "ERROR"}

                    if not response['data']:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)


                # Requisição 'search_favorite': busca nos favoritos e retorna os itens encontrados.
                elif data['action'] == 'search_favorite':
                    try:
                        query = db.search_favorites(data['user_id'], data['item_name'])
                        response = {"status": "OK", "data":[]}

                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})
                    
                    except:
                        response = {"status": "ERROR"}

                    if not response['data']:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)

                
                # Requisição 'update_item': atualiza um item cadastrado no catálogo.
                elif data['action'] == 'update_item':
                    try:
                        query = db.update_item(data['item_id'], data['item_name'], data['item_type'])
                        response = {"status": "OK"}

                    except:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)  


                # Requisição 'delete_item': deleta um item do catálogo.
                elif data['action'] == 'delete_item':
                    try:
                        query = db.delete_item(data['item_id'])
                        response = {"status": "OK"}
                    
                    except:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)
                
                
                # Requisição 'remove_favorite': remove um item dos favoritos do usuário.
                elif data['action'] == 'remove_favorite':
                    try:
                        query = db.delete_favorites(data['item_id'])
                        response = {"status": "OK"}
                    
                    except:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)


                # Recebeu uma requisição não esperada, retorna erro.
                else:
                    self.send_data(conn, {"status": "ERROR"})
                
                # Exibe o response da requisição recebida
                print(f"[LOG] Response: {response['status']}\n")
                db.close_connection()

        finally:
            self.clients.remove((conn, client_username))
            print(f'[!] Desconectando: ({addr,client_username})')
            conn.close()

def main():
    
    # Define porta e endereço do servidor
    PORT = 5050
    HOST = '127.0.0.1'
    server = ServerSocket(HOST, PORT)
    server.start_server()

if __name__ == "__main__":
    main()