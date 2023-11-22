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

    def opcao_selecionada(self):
        messagebox.showinfo("Opção Selecionada", "Funcionalidade em desenvolvimento.")

    def pop_table(self):
        self.tabela.delete(*self.tabela.get_children())

        # Solicita a ação query_all ao servidor e recebe os dados
        message = {'action':'query_all'}
        self.client_socket.send_data(message)
        data = self.client_socket.receive_data()
        
        if data:
            lista = data['data']
            for row in lista:
                r = list(row.values())
                self.tabela.insert('','end',values=r)


    def tela_catalogo(self):
        self.root = Tk()
        self.root.title('Listagem Catalogo')
        self.root.geometry('600x450')

        # Seção Catálogo
        area_catalogo = LabelFrame(self.root, text="Catalogo")
        area_catalogo.pack(fill="both", expand="yes", padx=10, pady=10)

        self.tabela = ttk.Treeview(area_catalogo, columns=('id', 'nome', 'tipo'), show='headings')
        self.tabela.column('id', minwidth=0, width=50)
        self.tabela.column('nome', minwidth=0, width=200)
        self.tabela.column('tipo', minwidth=0, width=80)
        self.tabela.heading('id', text='Id')
        self.tabela.heading('nome', text='Nome')
        self.tabela.heading('tipo', text='Tipo')
        self.tabela.pack()
        
        self.pop_table()
        
        # Seção adicionar
        area_add = LabelFrame(self.root, text='Adicionar item')
        area_add.pack(fill='both', expand='yes', padx=10, pady=10)
        
        label_nome = Label(area_add, text='Nome:')
        label_nome.pack(side='left')
        entry_nome = Entry(area_add)
        entry_nome.pack(side='left', padx=10)

        label_tipo = Label(area_add, text='Tipo:')
        label_tipo.pack(side='left')
        entry_nome = Entry(area_add)
        entry_nome.pack(side='left', padx=10)

        # Seção Pesquisar
        area_search = LabelFrame(self.root, text='Pesquisar')
        area_search.pack(fill='both', expand='yes', padx=10, pady=10)
        label_nome2 = Label(area_search, text='Nome:')
        label_nome2.pack(side='left')

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
