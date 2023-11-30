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

    def stop_server(self):
        self.server.close()

    def start_server(self):
        print("[!] O Servidor está inicializando...")
        print("[!] LOG Message format: [LOG] [{NOME}]: {MENSAGEM}")
        self.server.listen()

        print(f'[!] Servidor ativo [{self.ADDR[0]}]')

        # Inicializa o Banco de Dados do catálogo caso ele não exista
        self.ctlg = catalogo.Catalogo()
        self.ctlg._criar_tabelas()

        # Se os tipos não tiverem cadastrados, o cadastro é feito.
        # Tipos: (Filme, Serie, Anime, Outro)
        if not self.ctlg.query_types():
            self.ctlg._criar_tipos()

        self.ctlg.close_connection()

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[*] Conexões ativas: {threading.active_count() - 1}")

    def send_data(self, conn, data):
        message = json.dumps(data)
        conn.send(message.encode())

    def receive_data(self, conn):
        data = conn.recv(1024).decode()
        if data:
            data = json.loads(data)
        return data

    def handle_client(self, conn, addr):
        client_username = ''
        try:
            connected = True

            # Rececbe o nome do usuário
            data = self.receive_data(conn)
            client_username = data['username']
            self.clients.append((conn, client_username))

            db = catalogo.Catalogo()
            try:
                user = db.get_user_id(client_username)

                if not user:
                    try:
                        query = db.insert_user(client_username)
                        print('Usuario cadastrado: ', client_username)
                    
                    except:
                        print('Falha ao cadastrar usuario: ', client_username)

            except:
                print('FALHA AO BUSCAR CADASTRO')

            db.close_connection()
            
            # Mensagem de LOG
            print(f"[!] [+] ({addr}) {client_username} conectou-se.")

            while connected:

                # Recebe uma ação do cliente (requisição)
                data = self.receive_data(conn)
                if not data:
                    break
                
                # Conecta ao banco de dados
                db = catalogo.Catalogo()
                print(f'[LOG] ({addr}, {client_username}) : {data}')

                #------------------------------------- Todos os items
                if data['action'] == 'query_all':
                    try:
                        query = db.query_items()
                        response = {"status": "OK", "data":[]}

                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})

                    except:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)


                #------------------------------------- Inserir item
                elif data['action'] == 'insert_item':
                    try:
                        query = db.insert_item(data['item_name'], data['item_type'])
                        response = {"status": "OK"}

                    except:
                        print('ERRO AO CADASTRAR ITEM')
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)
                

                #------------------------------------- Buscar item
                elif data['action'] == 'search_item':
                    
                    try:
                        query = db.search_items(data['item_name'])
                        response = {"status": "OK", "data":[]}

                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})
                    
                    except:
                        print('ERRO AO BUSCAR ITEM')
                        print('Resposta: ', query)
                        response = {"status": "ERROR"}

                    if not response['data']:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)

                #------------------------------------- Deletar item
                elif data['action'] == 'delete_item':

                    try:
                        query = db.delete_item(data['item_id'])
                        response = {"status": "OK"}
                    
                    except:
                        print('ERRO AO DELETAR ITEM.')
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)
                

                #------------------------------------- Alterar item
                elif data['action'] == 'update_item':

                    try:
                        query = db.update_item(data['item_id'], data['item_name'], data['item_type'])
                        response = {"status": "OK"}

                    except:
                        print('ERRO AO ATUALIZAR ITEM.')
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)                        
                
                ##------------------------------------- Retornar id do usuário pelo nome
                elif data['action'] == 'get_userid':

                    try:
                        query = db.get_user_id(data['user_name'])
                        response = {"status": "OK", "data":[]}

                        for x in query:
                            response['data'].append({'user_id': x[0]})
                        
                    except:
                        print('ERRO AO BUSCAR ID DO USER')
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)
                
                ##------------------------------------- Insere item aos favoritos do usuario
                elif data['action'] == 'insert_favorite':
                    try:
                        # Verifica se o item ja foi cadastrado
                        query = db.was_favorited(data['user_id'], data['item_id'])

                        print('Resultado: ', query)
                        if not query:
                            try:
                                query = db.insert_favorites(data['user_id'], data['item_id'])
                                response = {"status": "OK"}

                            except:
                                print('ERRO AO CADASTRAR FAVORITO')
                                response = {"status": "ERROR"}

                        else:
                            response = {"status": "ERROR"}

                    except:
                        print('ERRO')

                    self.send_data(conn, response)
                
                ##------------------------------------- Remove item dos favoritos do usuario
                elif data['action'] == 'remove_favorite':
                    try:
                        query = db.delete_favorites(data['item_id'])
                        response = {"status": "OK"}
                    
                    except:
                        print('ERRO AO REMOVER ITEM DOS FAVORITOS.')
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)
                        
                        
                ##------------------------------------- Busca a lista de favoritos do usuario
                elif data['action'] == 'query_favorites':

                    try:
                        print('User de busca: ', data['user_id'])
                        query = db.query_favorites(data['user_id'])

                        response = {"status": "OK", "data":[]}
                        print('Resultado dos favoritos: ', query)
                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})

                        print('Valor de resposta ao buscar favoritos: ', response)
                    
                    except:
                        print('ERRO AO BUSCAR FAVORITOS')
                        response = {"status": "ERROR"}
                    
                    self.send_data(conn, response)

                elif data['action'] == 'search_favorite':

                    try:
                        query = db.search_favorites(data['user_id'], data['item_name'])
                        response = {"status": "OK", "data":[]}

                        for x in query:
                            response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})
                    
                    except:
                        print('ERRO AO BUSCAR ITEM FAVORITADO')
                        print('Resposta: ', query)
                        response = {"status": "ERROR"}

                    if not response['data']:
                        response = {"status": "ERROR"}

                    self.send_data(conn, response)


                else:
                    self.send_data(conn, {"status": "ERROR"})


        finally:
            self.clients.remove((conn, client_username))
            print(f'[LOG] Desconectando: ({addr,client_username})')
            conn.close()

def main():
    
    # Define porta e endereço do servidor
    PORT = 5050
    HOST = '127.0.0.1'
    server = ServerSocket(HOST, PORT)
    server.start_server()

if __name__ == "__main__":
    main()