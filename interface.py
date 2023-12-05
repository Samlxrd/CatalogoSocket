from tkinter import *
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
import client

class InterfaceGrafica:
    def __init__(self, SERVER, PORT):

        # Janela inicial que solicita um nome de usuário
        while True:
            self.nome_usuario = askstring("Nome de Usuário", "Digite seu nome de usuário:\t\t\t\t")
            if self.nome_usuario:
                break
            elif self.nome_usuario == None:
                return
            messagebox.showerror("NameError", "Nome de usuário não pode ser vazio.")

        # Realiza conexão com o servidor
        self.client_socket = client.ClientSocket(self.nome_usuario, SERVER, PORT)
        self.main_menu()


    # Tela principal, com as opções: Catalogo, Favoritos e Sair
    def main_menu(self):
        self.close_opened_window()

        self.root = Tk()
        self.root.title(f"Catalogo | Usuário: {self.nome_usuario}")
        self.root.geometry("350x216")
        self.root.resizable(False, False)

        # Salva o id do usuário para facilitar futuras requisições
        self.USERID = self.get_userid(self.nome_usuario)

        Button(self.root, text="Catalogo", font=('Comic-Sans', 12), command=self.tela_catalogo, width=16, pady=5).place(x=12*8,y=30)
        Button(self.root, text="Favoritos", font=('Comic-Sans', 12), command=self.tela_favoritos, width=16, pady=5).place(x=12*8,y=80)
        Button(self.root, text="Sair", font=('Comic-Sans', 12), command=self.root.destroy, width=16, pady=5).place(x=12*8,y=130)

        self.root.mainloop()


    # Função responsável por enviar uma requisição
    # ao servidor e retornar a resposta recebida.
    def request(self, message):
        self.client_socket.send_data(message)
        data = self.client_socket.receive_data()
        return data


    # Função para popular as tabelas (treeviews) da interface.
    def pop_table(self, query_type):

        # Limpa a tabela para evitar possiveis resultados duplicados
        self.tabela.delete(*self.tabela.get_children())

        # Envia requisição para buscar os dados no servidor ou de
        # todos os itens do catálogo ou dos favoritos do usuário.
        if query_type == 'query_favorites':
            data = self.request({"action": query_type, "user_id": self.USERID})
        else:
            data = self.request({"action": query_type})

        # Se teve sucesso ao buscar os dados, adiciona na tabela de exibição
        if data['status'] != 'ERROR':
            lista = data['data']
            for row in lista:
                r = list(row.values())
                self.tabela.insert('','end',values=r)


    # Evento acionado quando clicado em um item da tabela do catálogo
    def on_item_select(self, event):
        selecionado = self.tabela.focus()
        self.sel = self.tabela.item(selecionado)

        if self.sel['values']:
            self.button_editar['state'] = 'normal'
            self.button_excluir['state'] = 'normal'
            self.button_fav['state'] = 'normal'
        else:
            self.button_editar['state'] = 'disabled'
            self.button_excluir['state'] = 'disabled'
            self.button_fav['state'] = 'disabled'


    # Evento acionado quando clicado em um item da tabela dos favoritos
    def on_item_select_fav(self, event):
        selecionado = self.tabela.focus()
        self.sel = self.tabela.item(selecionado)

        if self.sel['values']:
            self.button_unfav['state'] = 'normal'
        else:
            self.button_unfav['state'] = 'disabled'


    # Evento acionado quando selecionado um tipo de item a ser cadastrado
    # Tipos: Filme, Série, Anime, Outro (Dispostos em uma combobox)
    def on_combobox_select(self, event):
        self.selected_type = self.type_select.get()


    # Função responsável por tratar e enviar ao servidor
    # a requisição de adicionar um item ao catálogo.
    def inserir(self, nome, tipo):

        # Verifica se todos os campos foram preenchidos
        if  nome == '':
            messagebox.showerror("FieldError", "Insira o nome do item a ser cadastrado.")
            return
        if  tipo == '':
            messagebox.showerror("FieldError", "Selecione o tipo de item a ser cadastrado.")
            return

        try: 
            tipo = self.tipos.index(tipo) + 1
        except ValueError:
            messagebox.showerror("FieldError", "Selecione corretamente um dos tipos da lista.")
            return
        
        # Envia requisição e recebe resposta do servidor
        response = self.request(message = {"action": "insert_item", "item_name": nome, "item_type": tipo})
        
        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Falha ao cadastrar o item.')
            return

        # Exibe mensagem de sucesso e popula a tabela com os dados recebidos.
        messagebox.showinfo(title='Mensagem do servidor', message='Item cadastrado com sucesso.')
        self.pop_table("query_all")


    # Função responsável por tratar e enviar ao servidor
    # a requisição de busca de itens no catálogo.
    def buscar(self, nome, query="search_item"):
        
        # Verifica se foi inserido texto no campo de busca.
        if nome == '':
            messagebox.showerror("FieldError", "Insira o nome do item a pesquisar")
            return
        
        # Envia requisição ao servidor de busca no catalogo
        # ou busca somente nos favoritos do usuário.
        if query == 'search_item':
            response = self.request(message = {"action": query, "item_name": nome})
        else:
            response = self.request(message = {"action": query, "user_id":self.USERID, "item_name": nome})

        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Item não encontrado.')
            return

        # Extrai os dados da resposta do servidor e exibe na tabela.
        data = response['data']
        self.show_search(data)   

    # Função responsável por tratar e enviar ao servidor
    # a requisição de exclusão de item do catálogo.
    def excluir(self, id):

        # Solicita que o usuário confirme que quer excluir o item.
        if not messagebox.askyesno(title='Mensagem do servidor', message='Tem certeza que quer excluir o item ?'):
            return

        # Envia requisição e recebe resposta do servidor
        response = self.request(message = {"action": "delete_item", "item_id": id})

        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Falha ao excluir o item do catálogo.')
            return
        
        # Remove o item da tabela
        self.tabela.delete(self.tabela.selection())

        # Exibe mensagem de sucesso.
        messagebox.showinfo(title='Mensagem do servidor', message='Item excluido com sucesso.')

    def editar(self, id, nome, tipo):

        # Solicita que o usuário confirme que quer alterar o item.
        if not messagebox.askyesno(title='Mensagem do servidor', message='Tem certeza que quer alterar o item ?'):
            return

        # Verifica se todos os campos foram preenchidos
        if  nome == '':
            messagebox.showerror("FieldError", "Insira o nome do item a ser atualizado.")
            return
        if  tipo == '':
            messagebox.showerror("FieldError", "Selecione o tipo de item a ser atualizado.")
            return
    
        try: 
            tipo = self.tipos.index(tipo) + 1

        except ValueError:
            messagebox.showerror("FieldError", "Selecione corretamente um dos tipos da lista.")
            return
        
        # Envia requisição e recebe resposta do servidor
        response = self.request(message = {"action" : "update_item", "item_id": id, "item_name": nome, "item_type": tipo})

        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Falha ao atualizar o item.')
            return

        # Exibe mensagem de sucesso.
        messagebox.showinfo(title='Mensagem do servidor', message='Item atualizado com sucesso.')

        self.tela_catalogo()

    # Função responsável por requisitar ao servidor o ID do cliente de acordo com o nome do usuário.
    def get_userid(self, username):
        
        # Envia requisição e recebe resposta do servidor
        response = self.request(message = {"action" : "get_userid", "user_name" : username})

        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Falha ao buscar id de usuário.')
            return
        
        # Retorna o id do usuário
        return response['data'][0]['user_id']

    # Função responsável por adicionar um item aos favoritos do usuário.
    def favoritar(self, item_id):

        # Solicita que o usuário confirme que quer adicionar o item aos favoritos.
        if not messagebox.askyesno(title='Mensagem do servidor', message='Deseja adicionar esse item aos favoritos?'):
            return
        
        # Envia requisição e recebe resposta do servidor.
        response = self.request(message = {"action" : "insert_favorite", "user_id": self.USERID, "item_id": item_id})

        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Falha ao favoritar o item.')
            return

        # Exibe mensagem de sucesso.
        messagebox.showinfo(title='Mensagem do servidor', message='Item adicionado aos favoritos.')

    # Função responsável por remover um item dos favoritos do usuário.
    def desfavoritar(self, item_id):

        # Solicita que o usuário confirme que quer remover o item dos favoritos.
        if not messagebox.askyesno(title='Mensagem do servidor', message='Deseja remover esse item dos favoritos?'):
            return
        
        # Envia requisição e recebe resposta do servidor.
        response = self.request(message = {"action" : "remove_favorite", "item_id": item_id})

        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Falha remover item dos favoritos.')
            return
        
        # Exibe mensagem de sucesso e remove o item da tabela de favoritos.
        messagebox.showinfo(title='Mensagem do servidor', message='Item removido dos favoritos.')
        self.tabela.delete(self.tabela.selection())


    # Função recebe dados (tuplas) e exibe na tabela da tela atual.
    def show_search(self, data):
        # Limpa a tabela para evitar possiveis resultados duplicados
        self.tabela.delete(*self.tabela.get_children())

        # Popula a tabela
        for row in data:
            r = list(row.values())
            self.tabela.insert('','end',values=r)


    # Função responsável por fechar a tela que está aberta no momento.
    def close_opened_window(self):
        try:
            self.root.destroy()
        except AttributeError:
            return


    # Função responsável por exibir a janela do catálogo
    # e todas suas funcionalidades disponíveis.
    def tela_catalogo(self):
        self.close_opened_window()

        self.root = Tk()
        self.root.title('Listagem Catalogo')
        self.root.resizable(False, False)
        self.root.geometry('600x550')

        # Seção Catálogo -------------------------------------------------------
        self.area_catalogo = LabelFrame(self.root, text="Catalogo")
        self.area_catalogo.pack(fill="both", expand="yes", padx=10, pady=10)

        # Cria a tabela que comportará os dados
        self.tabela = ttk.Treeview(self.area_catalogo, columns=('id', 'nome', 'tipo'), show='headings')
        self.tabela.column('id', minwidth=0, width=50)
        self.tabela.column('nome', minwidth=0, width=200)
        self.tabela.column('tipo', minwidth=0, width=80)
        self.tabela.heading('id', text='Id')
        self.tabela.heading('nome', text='Nome')
        self.tabela.heading('tipo', text='Tipo')
        self.tabela.pack(expand=True, side='left', ipadx=50)
        
        # Populando a tabela
        self.pop_table("query_all")
        self.tabela.bind('<<TreeviewSelect>>', self.on_item_select)

        # Adicionando a barra de rolagem
        scrollbar_y = ttk.Scrollbar(self.area_catalogo, orient="vertical", command=self.tabela.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tabela.configure(yscrollcommand=scrollbar_y.set)


        # Seção Opções ----------------------------------------------------------
        self.area_edit = LabelFrame(self.root, text="Opções")
        self.area_edit.pack(padx=10, ipady=10)

        # Botões Favoritar, Editar e Excluir
        self.button_fav = Button(self.area_edit, text='Favoritar', width=10, command=lambda: self.favoritar(self.sel['values'][0]))
        self.button_fav['state'] = 'disabled'
        self.button_fav.pack(side='left', padx=10)

        self.button_editar = Button(self.area_edit, text='Editar', width=10, command=lambda: self.tela_editar(self.sel['values']))
        self.button_editar['state'] = 'disabled'
        self.button_editar.pack(side='left', padx=10)

        self.button_excluir = Button(self.area_edit, text='Deletar', width=10, command=lambda: self.excluir(self.sel['values'][0]))
        self.button_excluir['state'] = 'disabled'
        self.button_excluir.pack(side='left', padx=10)
        

        # Seção adicionar -------------------------------------------------------
        area_add = LabelFrame(self.root, text='Adicionar item')
        area_add.pack(expand='yes', ipady=10)
        
        label_nome = Label(area_add, text='Nome:')
        label_nome.pack(side='left')
        entry_nome = Entry(area_add)
        entry_nome.pack(side='left', padx=10)

        label_tipo = Label(area_add, text='Tipo:')
        label_tipo.pack(side='left')

        self.tipos = ["Filme", "Série", "Anime", "Outro"]
        self.type_select = ttk.Combobox(area_add, value=self.tipos)
        self.type_select.pack(side='left', padx=10)
        self.type_select.bind("<<ComboboxSelected>>", self.on_combobox_select)

        button_inserir = Button(area_add, text='Adicionar', command=lambda: self.inserir(entry_nome.get(), self.type_select.get()))
        button_inserir.pack(side='left', padx=10)


        # Seção Pesquisar -------------------------------------------------------
        area_search = LabelFrame(self.root, text='Pesquisar item')
        area_search.pack(expand='yes', ipady=10)
        label_nome2 = Label(area_search, text='Nome:')
        label_nome2.pack(side='left')

        entry_nome2 = Entry(area_search)
        entry_nome2.pack(side='left', padx=10)

        button_pesquisar = Button(area_search, text='Buscar', command=lambda: self.buscar(entry_nome2.get()))
        button_pesquisar.pack(side='left', padx=10)

        button_mostrar_todos = Button(area_search, text='Mostrar Todos', command=lambda: self.pop_table("query_all"))
        button_mostrar_todos.pack(side='left', padx=10)

        button_voltar = Button(self.root, text='Voltar', command=self.main_menu, padx=30)
        button_voltar.pack(padx=10, pady=10)

        self.root.mainloop()


    # Função responsável por exibir uma pequena interface
    # para alteração de um item selecionado no catálogo.
    def tela_editar(self, fields):

        self.close_opened_window()
        
        self.root = Tk()
        self.root.title('Edição de Item')
        self.root.resizable(False, False)
        self.root.geometry('600x100')

        label_nome = Label(self.root, text='Nome:')
        label_nome.pack(side='left', padx=10)
        entry_nome = Entry(self.root)
        entry_nome.insert(0, fields[1])
        entry_nome.pack(side='left', padx=10)

        label_tipo = Label(self.root, text='Tipo:')
        label_tipo.pack(side='left')

        self.tipos = ["Filme", "Série", "Anime", "Outro"]
        self.type_select = ttk.Combobox(self.root, value=self.tipos)
        self.type_select.insert(0, fields[2])
        self.type_select.pack(side='left', padx=10)
        self.type_select.bind("<<ComboboxSelected>>", self.on_combobox_select)

        button_inserir = Button(self.root, text='Confirmar', width=10, command=lambda: self.editar(fields[0], entry_nome.get(), self.type_select.get()))
        button_inserir.pack(side='left', padx=10)

        button_cancelar = Button(self.root, text='Cancelar', width=10, command=self.tela_catalogo)
        button_cancelar.pack(side='left', padx=10)


    # Função responsável por exibir a janela dos itens favoritados
    # pelo usuário, permitindo buscar itens e desfavoritá-los.
    def tela_favoritos(self):
        self.close_opened_window()

        self.root = Tk()
        self.root.title(f'Meus Favoritos | Usuário: {self.nome_usuario}')
        self.root.resizable(False, False)
        self.root.geometry('600x550')

        # Seção Catálogo de Favoritos
        self.area_catalogo = LabelFrame(self.root, text="Catalogo")
        self.area_catalogo.pack(fill="both", expand="yes", padx=10, pady=10)

        self.tabela = ttk.Treeview(self.area_catalogo, columns=('id', 'nome', 'tipo'), show='headings')
        self.tabela.column('id', minwidth=0, width=50)
        self.tabela.column('nome', minwidth=0, width=200)
        self.tabela.column('tipo', minwidth=0, width=80)
        self.tabela.heading('id', text='Id')
        self.tabela.heading('nome', text='Nome')
        self.tabela.heading('tipo', text='Tipo')
        self.tabela.pack(expand=True, side='left', ipadx=50)
        
        # Populando a tabela com os itens favoritos do usuário
        self.pop_table("query_favorites")
        self.tabela.bind('<<TreeviewSelect>>', self.on_item_select_fav)

        # Adicionando a barra de rolagem
        scrollbar_y = ttk.Scrollbar(self.area_catalogo, orient="vertical", command=self.tabela.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tabela.configure(yscrollcommand=scrollbar_y.set)


        # Seção Opções ----------------------------------------------------------
        self.area_edit = LabelFrame(self.root, text="Opções")
        self.area_edit.pack(padx=20, ipady=10)

        # Botão Desfavoritar
        self.button_unfav = Button(self.area_edit, text='Remover dos Favoritos', width=20, command=lambda: self.desfavoritar(self.sel['values'][0]))
        self.button_unfav['state'] = 'disabled'
        self.button_unfav.pack(side='left', padx=10)


        # Seção Pesquisar -------------------------------------------------------
        area_search = LabelFrame(self.root, text='Pesquisar item')
        area_search.pack(expand='yes', ipady=10)
        label_nome2 = Label(area_search, text='Nome:')
        label_nome2.pack(side='left')

        entry_nome2 = Entry(area_search)
        entry_nome2.pack(side='left', padx=10)

        button_pesquisar = Button(area_search, text='Buscar', command=lambda: self.buscar(entry_nome2.get(), "search_favorite"))
        button_pesquisar.pack(side='left', padx=10)

        button_mostrar_todos = Button(area_search, text='Mostrar Todos', command=lambda: self.pop_table("query_favorites"))
        button_mostrar_todos.pack(side='left', padx=10)

        button_voltar = Button(self.root, text='Voltar', command=self.main_menu, padx=30)
        button_voltar.pack(padx=10, pady=10)

        self.root.mainloop()


def main():
    
    # Define porta e endereço do servidor
    PORT = 5050
    SERVER = '127.0.0.1'
    app = InterfaceGrafica(SERVER, PORT)
    while True:
        if not app:
            print('Aplicação encerrada.')

if __name__ == "__main__":
    main()
