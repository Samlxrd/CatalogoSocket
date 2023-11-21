from tkinter import *
from tkinter import messagebox, scrolledtext, ttk
from tkinter.simpledialog import askstring

class InterfaceGrafica:

    def __init__(self):

        while True:
            self.nome_cliente = askstring("Nome do Cliente", "Digite seu nome:\t\t\t\t")
            if self.nome_cliente:
                break
            elif self.nome_cliente == None:
                return
            messagebox.showerror("Erro", "Nome do cliente não pode ser vazio.")
        
        self.main_menu()
        

    def main_menu(self):
        self.root = Tk()
        self.root.title(f"Catalogo | Usuário: {self.nome_cliente}")
        self.root.geometry("540x324")
        self.root.resizable(False, False)

        #Label(self.root, text=f"Bem-vindo, {self.nome_cliente}").place(x=50,y=50)

        Button(self.root, text="Pesquisar", font=('Comic-Sans', 12), command=self.tela_pesquisar, width=16, pady=5).place(x=12*16,y=30)

        Button(self.root, text="Listar Catalogo", font=('Comic-Sans', 12), command=self.opcao_selecionada, width=16, pady=5).place(x=12*16,y=80)
        
        Button(self.root, text="Adicionar", font=('Comic-Sans', 12), command=self.opcao_selecionada, width=16, pady=5).place(x=12*16,y=130)

        Button(self.root, text="Favoritos", font=('Comic-Sans', 12), command=self.opcao_selecionada, width=16, pady=5).place(x=12*16,y=180)
        
        Button(self.root, text="Sair", font=('Comic-Sans', 12), command=self.root.destroy, width=16, pady=5).place(x=12*16,y=230)

        self.root.mainloop()


    def opcao_selecionada(self):
        messagebox.showinfo("Opção Selecionada", "Funcionalidade em desenvolvimento.")

    def tela_pesquisar(self):

        while True:
            self.search = askstring("Pesquisar", "Titulo:\t\t\t\t")
            if self.search:
                break
            elif self.search == None:
                return
            messagebox.showerror("Erro", "Digite algo para buscar.")
        
        self.mostrar_resultados_busca(self.search)

    def mostrar_resultados_busca(self, busca):
        # Chama método de envio
        self.root = Tk()

        catalogo = LabelFrame(self.root, text="Catalogo").pack(fill="both", expand="yes", padx=10, pady=10)

        tabela = ttk.Treeview(catalogo, columns=('id', 'nome', 'tipo'), show='headings')
        tabela.column('id', minwidth=0, width=50)
        tabela.column('nome', minwidth=0, width=200)
        tabela.column('tipo', minwidth=0, width=80)
        tabela.heading('id', text='Id')
        tabela.heading('nome', text='Nome')
        tabela.heading('tipo', text='Tipo')
        tabela.pack()


def main():
    app = InterfaceGrafica()

if __name__ == "__main__":
    main()
