from customtkinter import *
import os
from PIL import Image
from GerenciarEstoque import GerenciarEstoque
from Pesquisa import Pesquisa
from Users import Banco
from ParâmetrosJanelas import WindowParams
from LimparJanelas import LimparJanelas
from tkinter import messagebox
from deleteSystem32 import DeleteSystem32
from p import LivroFrame
from buscaApi import Busca


class ButtonFunctions:
    @staticmethod
    def delete_system(app):
        DeleteSystem32().delete()

    @staticmethod
    def login(app_instance):
        b = Banco()

        email = app_instance.email.get()
        senha = app_instance.senha.get()

        if email and senha:
            if b.login(email, senha):
                app_instance.janela_principal()
        else:
            print('aaaaaaaaa')
    
    @staticmethod
    def Cad(app_instance):
        b = Banco()

        email = app_instance.email_cad.get()
        senha = app_instance.senha_cad.get()

        if b.cadastro(email, senha):
            app_instance.janela_login

    @staticmethod
    def buscar_livro(app_instance):
        busca = Busca(app_instance)
        livro_buscado = app_instance.barra_pesquisa.get()

        if livro_buscado:
            busca.buscar(livro_buscado)
        else:
            messagebox.showerror(message=f'Não Temos o livro: {livro_buscado}')
            busca.exibir_bestsallers()

    @staticmethod
    def cadastro_livros(app):
        autor = app.autor.get()
        publicacao = app.publicação.get()
        titulo = app.obra.get()

        e = GerenciarEstoque()

        if autor and publicacao and titulo:
            e.CadastrarLivro(autor, titulo, publicacao)
        
        else:
            messagebox.showerror(title='erro', message='Preencha todos as campos!')

    @staticmethod
    def alterar_tabela(app):
        e = GerenciarEstoque()
        id = app.valor_alterado_id.get()
        valor_novo = app.valor_alterado.get()

        op = app.op.get()

        if op:
            if op == 'autor':
                e.AlterarAutor(valor_novo, int(id))
            if op == 'obra':
                e.AlterarObra(valor_novo, int(id))
            if op == 'publicação':
                e.AlterarAno(id, valor_novo)

    @staticmethod
    def consultar_tabela(app):
        e = GerenciarEstoque()

        e.ConsultarTabela()

    @staticmethod
    def busca_detalhada(app):
        p = Pesquisa()
        op = app.op.get()
        pesquisa = app.entry_pesquisa.get()
        
        if op:
            if op == 'obra':
                p.PesquisarPorObra(pesquisa)
            if op == 'autor':
                p.PesquisarPorAutor(pesquisa)
            if op == 'ID':
                p.PesquisarPorID(int(pesquisa))


class App(CTk, WindowParams, LimparJanelas):

    def __init__(self):
        super().__init__()
        self.janela_config()
        # self.janela_login()
        self.janela_principal()


    def janela_login(self):
        self.title('Login de Usuário')
        self.frame_login = CTkFrame(self, width=300, height=385, corner_radius=30)
        self.frame_login.place(x=394, y=8)

        self.img_logo = os.path.join(os.path.dirname(__file__), r'images/img_logo.png')
        
        self.img_logo = CTkImage(light_image=Image.open(self.img_logo), size=(160, 160))
        self.img_logo = CTkLabel(self.frame_login, text='', image=self.img_logo)
        self.img_logo.place(relx=0.5, rely=0.12, anchor=CENTER)

        self.email = CTkEntry(master=self.frame_login, placeholder_text='Seu e-mail', width=200, height=40, corner_radius=40, font=('archivo.ttf', 14))
        self.senha = CTkEntry(master=self.frame_login, placeholder_text='Sua senha', show='*', width=200, height=40, corner_radius=40, font=('archivo.ttf', 14))

        check_box = CTkCheckBox(master=self.frame_login, text="Lembrar login", font=('archivo.ttf', 14), corner_radius=30)
        check_box.place(relx=0.37, rely=0.55, anchor=CENTER)

        self.email.place(relx=0.5, rely=0.31, anchor=CENTER)
        self.senha.place(relx=0.5, rely=0.437, anchor=CENTER)

        self.label1 = CTkLabel(self, text="Faça login, ou cadastre-se, para acessar\n nossos serviços")
        self.label1.configure(font=('archivo.ttf', 17))
        self.label1.grid(row=0, column=0, padx=5, pady=25)

        self.image = os.path.join(os.path.dirname(__file__), r'images/img_login.png')
        self.image = CTkImage(light_image=Image.open(self.image), size=(300, 300))
        self.image = CTkLabel(self, text="", image=self.image)
        self.image.grid(row=1, column=0, padx=50, pady=0)

        botao_login = CTkButton(
    master=self.frame_login, 
    text='Fazer Login', 
    command=lambda: ButtonFunctions.login(self),
    width=200, 
    height=40, 
    corner_radius=40, 
    font=('archivo.ttf', 14)
)
        
        if botao_login._command == True:
            print('vasco')

        botao_login.place(relx=0.5, rely=0.67, anchor=CENTER)

        text_cad = CTkLabel(master=self.frame_login, text="Caso não tenha cadastro, cadastre-se.", font=('archivo.ttf', 14))
        text_cad.place(relx=0.5, rely=0.77, anchor=CENTER)

        botao_cadastro = CTkButton(self.frame_login, text="Cadastrar-se", fg_color='green', command=self.janela_cad, hover_color="dark green", width=200, height=40, corner_radius=40, font=('archivo.ttf', 14))

        botao_cadastro.place(relx=0.5, rely=0.87, anchor=CENTER)


    def janela_cad(self):
        self.frame_login.pack_forget()
        self.title('Cadastro de usuário')

        self.frame_cad = CTkFrame(self, width=300, height=385, corner_radius=30)
        self.frame_cad.place(x=394, y=8)

        self.img_logo = os.path.join(os.path.dirname(__file__),
                                     r'images/img_logo.png')
        self.img_logo = CTkImage(light_image=Image.open(self.img_logo), size=(160, 160))
        self.img_logo = CTkLabel(self.frame_cad, text='', image=self.img_logo)
        self.img_logo.place(relx=0.5, rely=0.12, anchor=CENTER)

        self.email_cad = CTkEntry(master=self.frame_cad, placeholder_text='Seu e-mail', width=200, height=40, corner_radius=40, font=('archivo.ttf', 14))

        self.senha_cad = CTkEntry(master=self.frame_cad, placeholder_text='Sua senha', show='*', width=200, height=40, corner_radius=40, font=('archivo.ttf', 14))

        check_box = CTkCheckBox(master=self.frame_cad, text="Mostrar senha", font=('archivo.ttf', 14), corner_radius=30, fg_color='green', hover_color='dark green')
        check_box.place(relx=0.37, rely=0.55, anchor=CENTER)

        self.email_cad.place(relx=0.5, rely=0.31, anchor=CENTER)
        self.senha_cad.place(relx=0.5, rely=0.437, anchor=CENTER)

        botao_cad = CTkButton(master=self.frame_cad, text='Finalizar cadastro', command=lambda: ButtonFunctions.Cad(self), width=200,                      height=40, corner_radius=40, font=('archivo.ttf', 14), fg_color='green', hover_color='dark green')
        botao_cad.place(relx=0.5, rely=0.66, anchor=CENTER)

        botao_voltar = CTkButton(master=self.frame_cad, text='Voltar ao login', command=self.janela_login, width=200,              height=40, corner_radius=40, font=('archivo.ttf', 14), fg_color='#444', hover_color='#333')
        botao_voltar.place(relx=0.5, rely=0.79, anchor=CENTER)

    def janela_principal(self):
        # self.frame_login.place_forget()
        # self.image.grid_forget()
        # self.label1.grid_forget()

        self.parametros_janela_principal()
        self.title('Sistema para Bibliotecas')

        self.frame = CTkFrame(master=self, width=300, height=590, corner_radius=15)
        self.frame.place(anchor=E, rely=0.5, relx=0.305)

        self.bestsellers = LivroFrame(parent=self)
        self.bestsellers.exibir_bestsallers()

        self.bestsellers.grid(row=1, column=1, padx=309, pady=80, sticky="nsew")

        usuario_image = os.path.join(os.path.dirname(__file__), r'images/img_usuário.png')
        usuario_image = CTkImage(light_image=Image.open(usuario_image), size=(40, 40))

        botão_perfil = CTkButton(master=self.frame, text='', fg_color='transparent', hover_color='#333',corner_radius=40, image=usuario_image, font=('archivo.ttf', 16), width=40, height=40)
        botão_perfil.place(relx=0.75, rely=0.0015, anchor=NW)

        config_image = os.path.join(os.path.dirname(__file__), r'images/img_config.png')
        config_image = CTkImage(light_image=Image.open(config_image), size=(40, 40))
        botão_config = CTkButton(master=self.frame, text='', image=config_image, width=6, fg_color='transparent',hover_color='#333', corner_radius=100, command=self.config)
        botão_config.place(relx=0, rely=0.0015, anchor=NW)

        self.barra_pesquisa = CTkEntry(master=self, placeholder_text='Pesquise em nosso sistema', width=400, height=40, corner_radius=50)
        self.barra_pesquisa.place(relx=0.619, rely=0.03, anchor=N)

        pesquisa_image = os.path.join(os.path.dirname(__file__), r'images/img_pesquisa.png')
        pesquisa_image = CTkImage(light_image=Image.open(pesquisa_image), size=(19, 20))
        self.botão_pesquisa = CTkButton(self, text="", width=20, height=40, fg_color='transparent', hover_color="#333", corner_radius=40, image=pesquisa_image, command=lambda: ButtonFunctions.buscar_livro(self))
        self.botão_pesquisa.place(relx=0.85, rely=0.03, anchor=N)

        img_banner = os.path.join(os.path.dirname(__file__),
                                  r'images/img_bannerbom.jpg')
        img_banner = CTkImage(light_image=Image.open(img_banner), size=(300, 87))
        img_banner = CTkLabel(master=self.frame, text="", image=img_banner)
        img_banner.place(relx=0.5, rely=0.18, anchor=CENTER)

        botão_empréstimo = CTkButton(master=self.frame, text='Solicitar empréstimo', fg_color='#333',hover_color='#363636', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14), command=self.janela_empréstimo)
        botão_empréstimo.place(relx=0.5, rely=0.33, anchor=CENTER)

        Empréstimos_solicitados = CTkButton(master=self.frame, text='Empréstimos solicitados', fg_color='#333',hover_color='#363636', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14), command=None)
        Empréstimos_solicitados.place(relx=0.5, rely=0.43, anchor=CENTER)

        botão_marketplace = CTkButton(master=self.frame, text='Cadastrar livros ', fg_color='#333',hover_color='#363636', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14), command=self.janela_cadastro_livro)
        botão_marketplace.place(relx=0.5, rely=0.53, anchor=CENTER)

        botão_compras = CTkButton(master=self.frame, text='Pesquisa detalhada', fg_color='#333',hover_color='#363636', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14), command=self.pesquisa_detalhada)
        botão_compras.place(relx=0.5, rely=0.63, anchor=CENTER)


    def pesquisa_detalhada(self):

        self.limpa_janela_principal()
        self.parametros_janela_principal()
        self.title('Pesquisa detalhada')

        valores = ['autor', 'obra', 'ID']

        #Frame Entradas e Botões:

        self.frame = CTkFrame(master=self, width=330, height=590, corner_radius=40)
        self.frame.place(anchor=E, rely=0.5, relx=0.995)

        #Botão Voltar:

        image_voltar = os.path.join(os.path.dirname(__file__), r'images/img_voltar.png')
        image_voltar = CTkImage(light_image=Image.open(image_voltar), size=(40, 40))
        self.botão_voltar = CTkButton(self, text='', image=image_voltar, width=6, fg_color='transparent', hover_color='#333', command=self.limpar_janela_pesquisa)
        self.botão_voltar.place(anchor=NE, relx=0.055, rely=0.01)

        #label Frame e Entries:

        CTkLabel(self.frame, text='Escolha por qual categoria\nvocê quer pesquisar!', font=('archivo.ttf', 18)).place(
            relx=0.5, rely=0.1, anchor=N)

        self.entry_pesquisa = CTkEntry(master=self.frame, placeholder_text='Item da busca.', width=280, height=45,
                                  corner_radius=40, font=('archivo.ttf', 14))
        self.entry_pesquisa.place(anchor=CENTER, rely=0.3, relx=0.5)

        #Menu que desce:

        self.op = StringVar(value=valores)
        option_menu = CTkOptionMenu(master=self.frame, values=valores, width=280, height=45, corner_radius=40, variable=self.op)
        # print(option_menu._values)
        option_menu.place(anchor=CENTER, rely=0.4, relx=0.5)
        option_menu.set('Escolher método')

        #Botões:

        CTkButton(self.frame, text='Realizar pesquisa.', fg_color='green', hover_color='dark green',
                  command=lambda: ButtonFunctions().busca_detalhada(self),
                  width=280, height=45, corner_radius=40, font=('archivo.ttf', 14)).place(anchor=CENTER,
                                                                                          rely=0.55, relx=0.5)

        CTkButton(self.frame, text='Voltar.', fg_color='#444', hover_color='#333', command=None,
                  width=280, height=45, corner_radius=40, font=('archivo.ttf', 14)).place(anchor=CENTER,
                                                                                          rely=0.65, relx=0.5)

        #Imagem e Label da Janela:

        self.label = CTkLabel(self, text='Hmmm vejo que você está atrás de algo mais específico!', font=('archivo.ttf', 18))
        self.label.place(anchor=N, relx=0.322, rely=0.1)

        self.image = os.path.join(os.path.dirname(__file__),
                                  r'images/pesquia_image 2.png')
        self.image = CTkImage(light_image=Image.open(self.image), size=(550, 366))

        self.label_image = CTkLabel(self, text="", image=self.image)
        self.label_image.place(anchor=N, relx=0.322, rely=0.2)


    def config(self):
        self.limpa_janela_principal()
        self.parametros_janela_principal()
        self.title('Configurções')

        image_voltar = os.path.join(os.path.dirname(__file__),
                                    r'images/img_voltar.png')
        image_voltar = CTkImage(light_image=Image.open(image_voltar), size=(40, 40))
        self.botão_voltar = CTkButton(self, text='', image=image_voltar, width=6, fg_color='transparent',
                                      hover_color='#333', command=self.limpar_janela_config)
        self.botão_voltar.place(anchor=NE, relx=0.055, rely=0.01)

        self.frame = CTkFrame(self, width=350, height=590, corner_radius=40)
        self.frame.place(anchor=CENTER, rely=0.5, relx=0.5)

        CTkLabel(self.frame, text='Alterar/ Remover dados do banco', font=('archivo.ttf', 16)).place(
            anchor=N, relx=0.5, rely=0.07)

        self.op = StringVar(value='Selecione')

        option_menu = CTkOptionMenu(master=self.frame, values=['autor', 'obra', 'publicação'], width=280, height=45, corner_radius=40, command=lambda _: ButtonFunctions.coluna(self), variable=self.op)
        option_menu.place(anchor=N, rely=0.18, relx=0.5)
        option_menu.set('Escolher coluna')

        self.valor_alterado = CTkEntry(self.frame, placeholder_text='Alteração', width=280, height=45, corner_radius=40)

        self.valor_alterado.place(anchor=N, rely=0.28, relx=0.5)

        self.valor_alterado_id = CTkEntry(self.frame, placeholder_text='ID', width=280, height=45, corner_radius=40)
        self.valor_alterado_id.place(anchor=N, rely=0.38, relx=0.5)

        button = CTkButton(self.frame, text='Fazer alteração', width=280, height=45, corner_radius=40,
                           font=('archivo.ttf', 14), fg_color='green', hover_color='dark green',
                           command=lambda: ButtonFunctions.alterar_tabela(self))
        button.place(anchor=CENTER, relx=0.501, rely=0.53)

        button = CTkButton(self.frame, text='Consultar tabela', width=280, height=45, corner_radius=40,
                           font=('archivo.ttf', 14), fg_color='#444', hover_color='#333', command=lambda: ButtonFunctions().consultar_tabela(self))
        button.place(anchor=CENTER, relx=0.501, rely=0.63)


    def janela_cadastro_livro(self):
        self.limpa_janela_principal()
        self.parametros_janela_principal()
        self.title('Cadastro de livros')

        self.frame_livro = CTkFrame(master=self, width=330, height=590, corner_radius=40)
        self.frame_livro.place(anchor=E, rely=0.5, relx=0.995)

        self.imagem = os.path.join(os.path.dirname(__file__),
                                   r'images/img_biblioteca.png')
        self.imagem = CTkImage(light_image=Image.open(self.imagem), size=(591, 422))
        self.imagem = CTkLabel(self, text='', image=self.imagem, )
        self.imagem.place(relx=0.6, rely=0.5, anchor=E)

        img_banner = os.path.join(os.path.dirname(__file__),
                                  r'images/img_bannerbom.jpg')
        img_banner = CTkImage(light_image=Image.open(img_banner), size=(330, 96))
        img_banner = CTkLabel(master=self.frame_livro, text="", image=img_banner)
        img_banner.place(relx=0.5, rely=0.18, anchor=CENTER)

        self.label = CTkLabel(self, text='Cadastre seu livro para\n outras pessoas poderem acessá-los! Ou, pesquise um livro!',
                              font=('archivo.ttf', 18))
        self.label.place(anchor=N, relx=0.325, rely=0.1)

        self.autor = CTkEntry(master=self.frame_livro, placeholder_text='Autor do livro', width=280, height=45,
                              corner_radius=40, font=('archivo.ttf', 14))
        self.obra = CTkEntry(master=self.frame_livro, placeholder_text='Título do livro', width=280, height=45,
                             corner_radius=40, font=('archivo.ttf', 14))
        self.publicação = CTkEntry(master=self.frame_livro, placeholder_text='Ano de publicação', width=280, height=45,
                                   corner_radius=40, font=('archivo.ttf', 14))
        self.ID = CTkEntry(master=self.frame_livro, placeholder_text='ID do livro (opicional)', width=280, height=45,
                           corner_radius=40, font=('archivo.ttf', 14))

        botão_cadastro = CTkButton(self.frame_livro, text='Cadastre seu livro!', width=280, height=45, corner_radius=40,
                                   font=('archivo.ttf', 14), fg_color='green', hover_color='dark green',
                                   command=lambda: ButtonFunctions.cadastro_livros(self))

        image_voltar = os.path.join(os.path.dirname(__file__),
                                    r'images/img_voltar.png')
        image_voltar = CTkImage(light_image=Image.open(image_voltar), size=(40, 40))
        self.botão_voltar = CTkButton(self, text='', image=image_voltar, width=6, fg_color='transparent',
                                      hover_color='#333',
                                      command=self.limpar_janela)
        self.botão_voltar.place(anchor=NE, relx=0.055, rely=0.01)

        self.autor.place(relx=0.5, rely=0.33, anchor=CENTER)
        self.obra.place(relx=0.5, rely=0.43, anchor=CENTER)
        self.publicação.place(relx=0.5, rely=0.53, anchor=CENTER)
        self.ID.place(relx=0.5, rely=0.63, anchor=CENTER)
        botão_cadastro.place(relx=0.5, rely=0.73, anchor=CENTER)


    def janela_empréstimo(self):

        self.limpa_janela_principal()
        self.parametros_janela_principal()
        self.title('Empréstimoms de livros')

        #Frame e Banner:

        self.frame_livro = CTkFrame(master=self, width=330, height=590, corner_radius=40)
        self.frame_livro.place(anchor=E, rely=0.5, relx=0.995)

        img_banner = os.path.join(os.path.dirname(__file__), r'images/img_bannerbom.jpg')
        img_banner = CTkImage(light_image=Image.open(img_banner), size=(330, 96))
        img_banner = CTkLabel(master=self.frame_livro, text="", image=img_banner)
        img_banner.place(relx=0.5, rely=0.18, anchor=CENTER)

        #Elementos Frame:

        self.entry = CTkEntry(self.frame_livro, placeholder_text='Livro Solicitado', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14))
        self.entry.place(anchor=CENTER, relx=0.501, rely=0.35)

        self.entry_id = CTkEntry(self.frame_livro, placeholder_text='ID Livro', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14))
        self.entry_id.place(anchor=CENTER, relx=0.501, rely=0.45)

        self.entry_senha = CTkEntry(self.frame_livro, placeholder_text='Senha Usuário', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14))
        self.entry_senha.place(anchor=CENTER, relx=0.501, rely=0.55)

        #Botão Empréstimo e Menu que desce:

        option_menu = CTkOptionMenu(master=self.frame_livro, values=['Prazo normal', 'Prazo extendido'], width=280, height=45,corner_radius=40)
        option_menu.place(anchor=CENTER, rely=0.65, relx=0.501)
        option_menu.set('Escolher prazo')

        button = CTkButton(self.frame_livro, text='Realizar empréstimo!', width=280, height=45, corner_radius=40, font=('archivo.ttf', 14), fg_color='green', hover_color='dark green', command=lambda : ButtonFunctions().delete_system(self))
        button.place(anchor=CENTER, relx=0.501, rely=0.75)

        #Botão Voltar:

        image_voltar = os.path.join(os.path.dirname(__file__), r'images/img_voltar.png')
        image_voltar = CTkImage(light_image=Image.open(image_voltar), size=(40, 40))
        self.botão_voltar = CTkButton(self, text='', image=image_voltar, width=6, fg_color='transparent', hover_color='#333', command=self.limpar_janela)
        self.botão_voltar.place(anchor=NE, relx=0.055, rely=0.01)

        #Imagem e Label:

        self.imagem = os.path.join(os.path.dirname(__file__), r'images/img_biblioteca.png')
        self.imagem = CTkImage(light_image=Image.open(self.imagem), size=(591, 422))
        self.imagem = CTkLabel(self, text='', image=self.imagem, )
        self.imagem.place(relx=0.6, rely=0.5, anchor=E)

        self.label = CTkLabel(self, text='Solicite o empréstimo do deu livro!', font=('archivo.ttf', 18))
        self.label.place(anchor=N, relx=0.325, rely=0.1)


if __name__ == "__main__":
    janela = App()
    janela.mainloop()