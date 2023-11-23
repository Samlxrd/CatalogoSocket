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

    def main_menu(self):
        self.root = Tk()
        self.root.title(f"Catalogo | Usuário: {self.nome_usuario}")
        self.root.geometry("540x324")
        self.root.resizable(False, False)

        #Label(self.root, text=f"Bem-vindo, {self.nome_usuario}").place(x=50,y=50)

        Button(self.root, text="Catalogo", font=('Comic-Sans', 12), command=self.tela_catalogo, width=16, pady=5).place(x=12*16,y=30)

        Button(self.root, text="Listar Catalogo", font=('Comic-Sans', 12), command=self.opcao_selecionada, width=16, pady=5).place(x=12*16,y=80)
        
        Button(self.root, text="Adicionar", font=('Comic-Sans', 12), command=self.opcao_selecionada, width=16, pady=5).place(x=12*16,y=130)

        Button(self.root, text="Favoritos", font=('Comic-Sans', 12), command=self.opcao_selecionada, width=16, pady=5).place(x=12*16,y=180)
        
        Button(self.root, text="Sair", font=('Comic-Sans', 12), command=self.root.destroy, width=16, pady=5).place(x=12*16,y=230)

        self.root.mainloop()

    def request(self, message):
        self.client_socket.send_data(message)
        data = self.client_socket.receive_data()
        return data

    def opcao_selecionada(self):
        messagebox.showinfo("Opção Selecionada", "Funcionalidade em desenvolvimento.")

    def pop_table(self):
        self.tabela.delete(*self.tabela.get_children())

        # Solicita a ação query_all ao servidor e recebe os dados
        data = self.request({"action": "query_all"})
        
        if data:
            lista = data['data']
            for row in lista:
                r = list(row.values())
                self.tabela.insert('','end',values=r)

    def on_item_select(self, event):
        selecionado = self.tabela.focus()
        print(selecionado)
        sel = self.tabela.item(selecionado)
        print(sel)

    def on_combobox_select(self, event):
        self.selected_type = self.type_select.get()
        print('Selecionado: ', self.selected_type)


    def inserir(self, nome, tipo):

        if  nome == '':
            messagebox.showerror("FieldError", "Insira o nome do item a ser cadastrado.")
            return
        if  tipo == '':
            messagebox.showerror("FieldError", "Selecione o tipo de item a ser cadastrado.")
            return
        
        tipo = self.tipos.index(tipo) + 1
        
        response = self.request(message = {"action": "insert_item", "item_name": nome, "item_type": tipo})
        if response['status'] == 'OK':
            messagebox.showinfo(title='Mensagem do servidor', message='Item cadastrado com sucesso.')
            self.pop_table()
        else:
            messagebox.showwarning(title='Mensagem do servidor', message='Falha ao cadastrar o item.')

    def buscar(self, nome):

        if nome == '':
            messagebox.showerror("FieldError", "Insira o nome do item a pesquisar")
            return
        
        response = self.request(message = {"action": "search_item", "item_name": nome})

        if response['status'] == 'ERROR':
            messagebox.showwarning(title='Mensagem do servidor', message='Item não encontrado no catálogo.')
            return

        data = response['data']
        self.show_search(data)   

    def show_search(self, data):
        self.tabela.delete(*self.tabela.get_children())

        for row in data:
            r = list(row.values())
            self.tabela.insert('','end',values=r)


    def tela_catalogo(self):
        self.root.destroy()

        self.root = Tk()
        self.root.title('Listagem Catalogo')
        self.root.geometry('600x450')

        # Seção Catálogo
        self.area_catalogo = LabelFrame(self.root, text="Catalogo")
        self.area_catalogo.pack(fill="both", expand="yes", padx=10, pady=10)

        self.tabela = ttk.Treeview(self.area_catalogo, columns=('id', 'nome', 'tipo'), show='headings')
        self.tabela.column('id', minwidth=0, width=50)
        self.tabela.column('nome', minwidth=0, width=200)
        self.tabela.column('tipo', minwidth=0, width=80)
        self.tabela.heading('id', text='Id')
        self.tabela.heading('nome', text='Nome')
        self.tabela.heading('tipo', text='Tipo')
        self.tabela.pack()
        
        self.pop_table()
        self.tabela.bind('<<TreeviewSelect>>', self.on_item_select)
        
        # Seção adicionar
        area_add = LabelFrame(self.root, text='Adicionar item')
        area_add.pack(fill='both', expand='yes', padx=10, pady=10)
        
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

        # Seção Pesquisar
        area_search = LabelFrame(self.root, text='Pesquisar')
        area_search.pack(fill='both', expand='yes', padx=10, pady=10)
        label_nome2 = Label(area_search, text='Nome:')
        label_nome2.pack(side='left')

        entry_nome2 = Entry(area_search)
        entry_nome2.pack(side='left', padx=10)

        button_pesquisar = Button(area_search, text='Buscar', command=lambda: self.buscar(entry_nome2.get()))
        button_pesquisar.pack(side='left', padx=10)

        self.root.mainloop()


def main():
    
    # Define porta e endereço do servidor
    PORT = 5050
    SERVER = '127.0.0.1'
    app = InterfaceGrafica(SERVER, PORT)
    while True:
        if not app:
            print('fechou')

if __name__ == "__main__":
    main()
