from customtkinter import *
import os
import sqlite3 as sq
from PIL import Image
from tkinter import END
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter as tk


class Banco():
    def conn_db(self):
        self.conn = sq.connect('acessos.db')
        self.cursor = self.conn.cursor()
        print('Banco conectado com sucesso!')

    def desconn_db(self):
        self.conn.close()
        print('Banco desconectado com sucesso!')

    def criar_tabela(self):
        self.conn_db()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS acessos (
                'email' text not null,
                'senha' text not null
            )
            ''')

        self.conn.commit()
        print('Tabela criada com sucesso!')
        self.desconn_db()

    def cadastro(self):
        self.email_cadastro = self.email_cad.get()
        self.senha_cadastro = self.senha_cad.get()

        self.conn_db()

        self.cursor.execute("INSERT INTO acessos VALUES (?, ?)",
                            (self.email_cadastro, self.senha_cadastro))

        a = 0

        for i in self.senha_cadastro:
            a += 1
        print(a)

        try:
            if a < 5:
                messagebox.showinfo(title='Login', message='Por favor, faça uma senha com mais de cinco caracteres.')
            else:
                self.conn.commit()
                messagebox.showinfo(title='Login', message='Cadastro efetuado com sucesso!\n'
                                                           ' Volte à tela de login para efetuá-lo')
                self.desconn_db()
                self.limpa_cadastro()
            if self.senha_cadastro == '' or self.email_cadastro == '':
                messagebox.showinfo(title='Login', message='Percebi que alguns espaços estão vazios. Preencha TODOS!')
            else:
                self.conn.commit()
                messagebox.showinfo(title='Login', message='Cadastro efetuado com sucesso!\n'
                                                           ' Volte à tela de login para efetuá-lo')
                self.desconn_db()
                self.limpa_cadastro()
        except:
            pass

    def login(self):
        self.email_log = self.email.get()
        self.senha_log = self.senha.get()

        self.conn_db()
        self.cursor.execute('''SELECT * FROM acessos WHERE email = ? AND senha = ?''',
                            (self.email_log, self.senha_log))

        self.resultado = self.cursor.fetchone()
        print('Validando dados')
        self.desconn_db()

        if self.resultado:
            self.janela_principal()
        else:
            messagebox.showinfo(title='Login', message='Ocorreu um erro, por favor, tente novamente.'
                                                       '\nCaso não tenha cadastro, cadastre-se!')


class Livros():

    def coluna(self, método):
        self.método = método
        print(self.método)

    def conn_db(self):
        self.conn = sq.connect('livros_projeto.db')
        self.cursor = self.conn.cursor()
        print('Tabela "livros_projeto" conectada com sucesso!')
    def desconn_db(self):
        self.conn.close()
        print('Banco desconectado com sucesso!')

    def criar_tabela_livros(self):
        self.conn_db()
        try:
            self.cursor.execute('''
                CREATE TABLE livros_projeto (
                    autor text,
                    obra text,
                    publicação text,
                    ID text
                )
                ''')

            print('comando SQL:', self.cursor)

            self.conn.commit()
            print('Tabela "livros_projeto.db" criada com sucesso!')
            self.desconn_db()
        except sq.OperationalError:
            print('a tabela está "criada"')
            print('O banco está em:', self.conn)


            self.conn_db()
            self.cursor.execute('SELECT * FROM livros_projeto')

            valores = self.cursor.fetchall()

            print('Valores:')
            for valor in valores:
                print(valor)

            self.desconn_db()

    def cadastro_livros(self):
        try:
            self.autor_livro = self.autor.get()
            self.publicacao_livro = self.publicação.get()
            self.titulo_obra = self.obra.get()
            self.id_obra = self.ID.get()

            self.conn_db()

            if self.autor_livro and self.publicacao_livro and self.titulo_obra and self.id_obra:
                self.cursor.execute("INSERT INTO livros_projeto VALUES (?, ?, ?, ?)",
                                    (self.autor_livro, self.titulo_obra,self.publicacao_livro, self.id_obra))
                print(self.autor_livro, self.titulo_obra, self.publicacao_livro, self.id_obra)
                self.conn.commit()
                messagebox.showinfo(title='Cadastro concluído!', message='Cadastramos o seu livro com sucesso!')
            else:
                messagebox.showwarning(title='Campos vazios', message='Atenção! Todos os campos necessitam de preenchimento!')

        except sq.Error as e:
            messagebox.showerror(title='ERROR!', message=f'ERREOR: {e}')

        finally:
            self.desconn_db()

    def alterar_tabela(self):
        self.id = self.valor_alterado_id.get()

        self.valor_novo = self.valor_alterado.get()
        print(self.valor_novo, self.id)

        self.conn_db()
        self.cursor.execute(f'update livros_projeto set {self.método} = "{self.valor_novo}" where ID = "{self.id}"')

        self.conn.commit()
        self.conn.close()

    def consultar_tabela(self):
        self.conn_db()
        self.cursor.execute('select * from livros_projeto')
        valores = self.cursor.fetchall()

        janela_resultado = tk.Toplevel()
        janela_resultado.resizable(width=False, height=False)

        text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=40, height=10)
        text_resultado.pack(padx=10, pady=10)

        text_resultado.insert(tk.END, f"{'Resultado(s) mais coerente(s)':<30}")
        text_resultado.insert(tk.END, "-" * 80 + "\n")

        for valor in valores:
            text_resultado.insert(tk.END,
                                  f'Livro: {valor[1]};\nAutor: {valor[0]};\nPublicação: {valor[2]};\nID: {valor[3]}\n\n')

        self.desconn_db()


class Pesquisa():

    def detalhe_pesquisa(self):
        self.pesquisa = self.entry_pesquisa.get()
        self.método_pesquisa = self.método
        print(self.método_pesquisa)

    def método_pesquisa(self, método):
        self.método = método
        print(f'método de pesquisa: {self.método}')

    def livro_buscado(self):
        self.busca = self.barra_pesquisa.get()

    def conn_db(self):
        self.conn = sq.connect('livros_projeto.db')
        self.cursor = self.conn.cursor()

        print('Tabela pesquisa conectada com sucesso!')

    def desconn_db(self):
        self.conn.close()
        print('Tabela pesquisa desconectada com sucessso!')

    def buscar_livro(self):
        try:
            self.livro_buscado()
            self.conn_db()

            print('Sua pesquisa foi:', self.busca)
            self.cursor.execute(f'SELECT * FROM livros_projeto WHERE LOWER(obra) LIKE "%{self.busca}%"')
            self.resultado = self.cursor.fetchall()

            if self.resultado:
                janela_resultado = tk.Toplevel()
                janela_resultado.resizable(width=False, height=False)

                text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=40, height=10)
                text_resultado.pack(padx=10, pady=10)

                text_resultado.insert(tk.END, f"{'Resultado(s) mais coerente(s)':<30}")
                text_resultado.insert(tk.END, "-" * 80 + "\n")

                for resultado in self.resultado:
                    text_resultado.insert(tk.END,
                                          f'Livro: {resultado[1]};\nAutor: {resultado[0]};\nPublicação: {resultado[2]};\nID: {resultado[3]}\n\n' )

                # messagebox.showinfo(title='Busca de livros', message='Temos algumas unidades deste livro sim!')
            else:
                messagebox.showinfo(title='Busca de livros', message="Infelizmente, não temos este livro =,(")

        except sq.Error as e:
            print('O erro foi:', e)
            print(f'Consulta SQL: SELECT * FROM livros_projeto WHERE LOWER(obra) LIKE "%{self.busca}%"')

        finally:
            self.desconn_db()
            self.barra_pesquisa.delete(0, END)

    def busca_detalhada(self):
        self.detalhe_pesquisa()
        self.conn_db()

        try:
            if self.método == 'ID':
                print(type(self.método))
                print(self.pesquisa)
                self.cursor.execute(f'select * from livros_projeto where {self.método} = "{self.pesquisa}"')
                self.resultado = self.cursor.fetchall()

                if self.resultado:
                    janela_resultado = tk.Toplevel()
                    janela_resultado.resizable(width=False, height=False)

                    text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=40, height=10)
                    text_resultado.pack(padx=10, pady=10)

                    text_resultado.insert(tk.END, f"{'Resultado:':<30}")
                    text_resultado.insert(tk.END, "-" * 80 + "\n")

                    for resultado in self.resultado:
                        text_resultado.insert(tk.END,
                                              f'Autor: {resultado[0]};\nLivro: {resultado[1]};\nPublicação: {resultado[2]};\nID: {resultado[3]}\n\n')

                if not self.resultado:
                    messagebox.showinfo(title='Resultado', message='Não encontramos um resultado para este ID!')



            else:
                self.cursor.execute(f'select * from livros_projeto where {self.método} like "%{self.pesquisa}%"')
                self.resultado = self.cursor.fetchall()

                if self.resultado:
                    print('encontramos algo.')
                else:
                    print('Não temos resultados')

                if self.resultado and self.método == 'autor':

                    janela_resultado = tk.Toplevel()
                    janela_resultado.resizable(width=False, height=False)

                    text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=40, height=10)
                    text_resultado.pack(padx=10, pady=10)

                    text_resultado.insert(tk.END, f"{'Possíveis resultados:':<30}")
                    text_resultado.insert(tk.END, "-" * 80 + "\n")

                    for resultado in self.resultado:
                        text_resultado.insert(tk.END,
                                              f'Autor: {resultado[0]};\nLivro: {resultado[1]}.\n\n')

                elif self.resultado and self.método == 'obra':

                    janela_resultado = tk.Toplevel()
                    janela_resultado.resizable(width=False, height=False)

                    text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=40, height=10)
                    text_resultado.pack(padx=10, pady=10)

                    text_resultado.insert(tk.END, f"{'Possíveis resultados:':<30}")
                    text_resultado.insert(tk.END, "-" * 80 + "\n")

                    for resultado in self.resultado:
                        text_resultado.insert(tk.END,
                                              f'Livro: {resultado[1]};\nAutor: {resultado[0]}.\n\n')

                elif self.resultado and self.método == 'publicação':

                    janela_resultado = tk.Toplevel()
                    janela_resultado.resizable(width=False, height=False)

                    text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=40, height=10)
                    text_resultado.pack(padx=10, pady=10)

                    text_resultado.insert(tk.END, f"{'Possíveis resultados:':<30}")
                    text_resultado.insert(tk.END, "-" * 80 + "\n")

                    for resultado in self.resultado:
                        text_resultado.insert(tk.END,
                                              f'Livro: {resultado[1]};\nPublicação: {resultado[2]};\nAutor: {resultado[0]}.\n\n')

                else:
                    messagebox.showerror(title='ERROR!', message='Infelizmente ocorreu um erro, por favor, tente novamente.')

        except sq.Error as e:
            print(f'erro de: {e}')

        finally:
            self.desconn_db()


class App(CTk, Banco, Livros, Pesquisa):

    def __init__(self):
        super().__init__()
        # self.janela_principal()
        self.criar_tabela()
        self.janela_config()
        self.janela_login()
        self.criar_tabela_livros()
        # self.pesquisa_detalhada()
        self.iconbitmap(self, r'images\img_001.ico')

    def janela_config(self):
        self.geometry("700x400")
        self.resizable(width=False, height=False)

    def janela_login(self):
        self.title('Login de Usuário')
        self.frame_login = CTkFrame(self, width=300, height=385, corner_radius=30)
        self.frame_login.place(x=394, y=8)

        self.img_logo = os.path.join(os.path.dirname(__file__),
                                     r'images\img_logo.png')
        self.img_logo = CTkImage(light_image=Image.open(self.img_logo), size=(160, 160))
        self.img_logo = CTkLabel(self.frame_login, text='', image=self.img_logo)
        self.img_logo.place(relx=0.5, rely=0.12, anchor=CENTER)

        self.email = CTkEntry(master=self.frame_login, placeholder_text='Seu e-mail', width=200, height=40,
                              corner_radius=40, font=('archivo.ttf', 14))
        self.senha = CTkEntry(master=self.frame_login, placeholder_text='Sua senha', show='*', width=200,
                              height=40, corner_radius=40, font=('archivo.ttf', 14))

        check_box = CTkCheckBox(master=self.frame_login, text="Lembrar login", font=('archivo.ttf', 14),
                                corner_radius=30)
        check_box.place(relx=0.37, rely=0.55, anchor=CENTER)

        self.email.place(relx=0.5, rely=0.31, anchor=CENTER)
        self.senha.place(relx=0.5, rely=0.437, anchor=CENTER)

        self.label1 = CTkLabel(self, text="Faça login, ou cadastre-se, para acessar\n nossos serviços")
        self.label1.configure(font=('archivo.ttf', 17))
        self.label1.grid(row=0, column=0, padx=5, pady=25)

        self.image = os.path.join(os.path.dirname(__file__),
                                  r'images\img_login.png')
        self.image = CTkImage(light_image=Image.open(self.image), size=(300, 300))
        self.image = CTkLabel(self, text="", image=self.image)
        self.image.grid(row=1, column=0, padx=50, pady=0)

        botao_login = CTkButton(master=self.frame_login, text='Fazer Login', command=self.login, width=200, height=40,
                                corner_radius=40, font=('archivo.ttf', 14))

        botao_login.place(relx=0.5, rely=0.67, anchor=CENTER)

        text_cad = CTkLabel(master=self.frame_login, text="Caso não tenha cadastro, cadastre-se.",
                            font=('archivo.ttf', 14))
        text_cad.place(relx=0.5, rely=0.77, anchor=CENTER)

        botao_cadastro = CTkButton(self.frame_login, text="Cadastrar-se", fg_color='green', command=self.janela_cad,
                                   hover_color="dark green", width=200, height=40, corner_radius=40,
                                   font=('archivo.ttf', 14))

        botao_cadastro.place(relx=0.5, rely=0.87, anchor=CENTER)

    def janela_cad(self):
        self.frame_login.pack_forget()
        self.title('Cadastro de usuário')

        self.frame_cad = CTkFrame(self, width=300, height=385, corner_radius=30)
        self.frame_cad.place(x=394, y=8)

        self.img_logo = os.path.join(os.path.dirname(__file__),
                                     r'images\img_logo.png')
        self.img_logo = CTkImage(light_image=Image.open(self.img_logo), size=(160, 160))
        self.img_logo = CTkLabel(self.frame_cad, text='', image=self.img_logo)
        self.img_logo.place(relx=0.5, rely=0.12, anchor=CENTER)

        self.email_cad = CTkEntry(master=self.frame_cad, placeholder_text='Seu e-mail', width=200, height=40,
                                  corner_radius=40,
                                  font=('archivo.ttf', 14))

        self.senha_cad = CTkEntry(master=self.frame_cad, placeholder_text='Sua senha', show='*', width=200, height=40,
                                  corner_radius=40, font=('archivo.ttf', 14))

        check_box = CTkCheckBox(master=self.frame_cad, text="Mostrar senha", font=('archivo.ttf', 14), corner_radius=30,
                                fg_color='green', hover_color='dark green')
        check_box.place(relx=0.37, rely=0.55, anchor=CENTER)

        self.email_cad.place(relx=0.5, rely=0.31, anchor=CENTER)
        self.senha_cad.place(relx=0.5, rely=0.437, anchor=CENTER)

        botao_cad = CTkButton(master=self.frame_cad, text='Finalizar cadastro', command=self.cadastro, width=200,
                              height=40,
                              corner_radius=40, font=('archivo.ttf', 14), fg_color='green', hover_color='dark green')
        botao_cad.place(relx=0.5, rely=0.66, anchor=CENTER)

        botao_voltar = CTkButton(master=self.frame_cad, text='Voltar ao login', command=self.janela_login, width=200,
                                 height=40, corner_radius=40, font=('archivo.ttf', 14), fg_color='#444',
                                 hover_color='#333')
        botao_voltar.place(relx=0.5, rely=0.79, anchor=CENTER)

    def limpa_janela_principal(self):
        self.frame.place_forget()
        self.barra_pesquisa.place_forget()
        self.botão_pesquisa.place_forget()
        self.label.place_forget()
        self.label_imagem.place_forget()

    def limpar_janela_pesquisa(self):
        self.frame.place_forget()
        self.botão_voltar.place_forget()
        self.label_image.place_forget()
        self.label.place_forget()
        self.janela_principal()

    def limpar_janela(self):
        self.frame_livro.place_forget()
        self.imagem.place_forget()
        self.botão_voltar.place_forget()
        self.label.place_forget()

        self.janela_principal()

    def limpar_janela_config(self):
        self.frame.place_forget()
        self.botão_voltar.place_forget()

        self.janela_principal()

    def parametros_janela_principal(self):
        self.geometry('1000x600')
        self.resizable(False, False)
        self.iconbitmap(r'images\img_001.ico')

    def janela_principal(self):
        self.frame_login.place_forget()
        self.image.grid_forget()
        self.label1.grid_forget()

        self.parametros_janela_principal()
        self.title('Sistema para Bibliotecas')

        self.frame = CTkFrame(master=self, width=300, height=590, corner_radius=40)
        self.frame.place(anchor=E, rely=0.5, relx=0.305)

        imagem_principal = os.path.join(os.path.dirname(__file__),
                                        r'images\img_biblioteca_02.png')
        imagem_principal = CTkImage(light_image=Image.open(imagem_principal), size=(591, 422))
        self.label_imagem = CTkLabel(self, text='', image=imagem_principal)
        self.label_imagem.place(relx=0.619, rely=0.5, anchor=CENTER)

        # self.barra = CTkScrollbar(master=self, fg_color='#333')
        # self.barra.pack(side='right', fill='y')

        usuario_image = os.path.join(os.path.dirname(__file__),
                                     r'images\img_usuário.png')
        usuario_image = CTkImage(light_image=Image.open(usuario_image), size=(40, 40))

        botão_perfil = CTkButton(master=self.frame, text='', fg_color='transparent', hover_color='#333',
                                 corner_radius=20, image=usuario_image, font=('archivo.ttf', 16), width=5)
        botão_perfil.place(relx=0.75, rely=0.0015, anchor=NW)

        config_image = os.path.join(os.path.dirname(__file__),
                                    r'images\img_config.png')
        config_image = CTkImage(light_image=Image.open(config_image), size=(40, 40))
        botão_config = CTkButton(master=self.frame, text='', image=config_image, width=6, fg_color='transparent',
                                 hover_color='#333', corner_radius=100, command=self.config)
        botão_config.place(relx=0, rely=0.0015, anchor=NW)

        self.barra_pesquisa = CTkEntry(master=self, placeholder_text='Pesquise em nosso sistema', width=400, height=40,
                                       corner_radius=50)
        self.barra_pesquisa.place(relx=0.619, rely=0.03, anchor=N)

        pesquisa_image = os.path.join(os.path.dirname(__file__),
                                      r'images\img_pesquisa.png')
        pesquisa_image = CTkImage(light_image=Image.open(pesquisa_image), size=(19, 20))
        self.botão_pesquisa = CTkButton(self, text="", width=20, height=40, fg_color='transparent', hover_color="#333",
                                        corner_radius=40, image=pesquisa_image, command=self.buscar_livro)
        self.botão_pesquisa.place(relx=0.85, rely=0.03, anchor=N)

        self.label = CTkLabel(self, text='Sistema para Bibliotécas!', font=('archivo.ttf', 16))
        self.label.place(relx=0.616, rely=0.9, anchor=CENTER)
        # self.label.place_forget()

        img_banner = os.path.join(os.path.dirname(__file__),
                                  r'images\img_bannerbom.jpg')
        img_banner = CTkImage(light_image=Image.open(img_banner), size=(300, 87))
        img_banner = CTkLabel(master=self.frame, text="", image=img_banner)
        img_banner.place(relx=0.5, rely=0.18, anchor=CENTER)

        botão_empréstimo = CTkButton(master=self.frame, text='Solicitar empréstimo', fg_color='#333',
                                     hover_color='#363636', width=280, height=45, corner_radius=40,
                                     font=('archivo.ttf', 14),
                                     command=self.janela_empréstimo)
        botão_empréstimo.place(relx=0.5, rely=0.33, anchor=CENTER)

        Empréstimos_solicitados = CTkButton(master=self.frame, text='Empréstimos solicitados', fg_color='#333',
                                            hover_color='#363636', width=280, height=45, corner_radius=40,
                                            font=('archivo.ttf', 14), command=None)
        Empréstimos_solicitados.place(relx=0.5, rely=0.43, anchor=CENTER)

        botão_marketplace = CTkButton(master=self.frame, text='Cadastrar livros ', fg_color='#333',
                                      hover_color='#363636', width=280, height=45, corner_radius=40,
                                      font=('archivo.ttf', 14), command=self.janela_cadastro_livro)
        botão_marketplace.place(relx=0.5, rely=0.53, anchor=CENTER)

        botão_compras = CTkButton(master=self.frame, text='Pesquisa detalhada', fg_color='#333',
                                  hover_color='#363636', width=280, height=45, corner_radius=40,
                                  font=('archivo.ttf', 14), command=self.pesquisa_detalhada)
        botão_compras.place(relx=0.5, rely=0.63, anchor=CENTER)

    def pesquisa_detalhada(self):

        self.limpa_janela_principal()
        self.parametros_janela_principal()
        self.title('Pesquisa detalhada')

        valores = ['autor', 'obra', 'publicação', 'ID']

        #Frame Entradas e Botões:

        self.frame = CTkFrame(master=self, width=330, height=590, corner_radius=40)
        self.frame.place(anchor=E, rely=0.5, relx=0.995)

        #Botão Voltar:

        image_voltar = os.path.join(os.path.dirname(__file__),
                                    r'images\img_voltar.png')
        image_voltar = CTkImage(light_image=Image.open(image_voltar), size=(40, 40))
        self.botão_voltar = CTkButton(self, text='', image=image_voltar, width=6, fg_color='transparent',
                                      hover_color='#333',
                                      command=self.limpar_janela_pesquisa)
        self.botão_voltar.place(anchor=NE, relx=0.055, rely=0.01)

        #label Frame e Entries:

        CTkLabel(self.frame, text='Escolha por qual categoria\nvocê quer pesquisar!', font=('archivo.ttf', 18)).place(
            relx=0.5, rely=0.1, anchor=N)

        self.entry_pesquisa = CTkEntry(master=self.frame, placeholder_text='Item da busca.', width=280, height=45,
                                  corner_radius=40, font=('archivo.ttf', 14))
        self.entry_pesquisa.place(anchor=CENTER, rely=0.3, relx=0.5)

        #Menu que desce:

        option_menu = CTkOptionMenu(master=self.frame, values=valores, width=280, height=45, corner_radius=40,
                                    command=self.método_pesquisa)
        option_menu.place(anchor=CENTER, rely=0.4, relx=0.5)
        option_menu.set('Escolher método')

        #Botões:

        CTkButton(self.frame, text='Realizar pesquisa.', fg_color='green', hover_color='dark green',
                  command=self.busca_detalhada,
                  width=280, height=45, corner_radius=40, font=('archivo.ttf', 14)).place(anchor=CENTER,
                                                                                          rely=0.55, relx=0.5)

        CTkButton(self.frame, text='Voltar.', fg_color='#444', hover_color='#333', command=None,
                  width=280, height=45, corner_radius=40, font=('archivo.ttf', 14)).place(anchor=CENTER,
                                                                                          rely=0.65, relx=0.5)

        #Imagem e Label da Janela:

        self.label = CTkLabel(self, text='Hmmm vejo que você está atrás de algo mais específico!', font=('archivo.ttf', 18))
        self.label.place(anchor=N, relx=0.322, rely=0.1)

        self.image = os.path.join(os.path.dirname(__file__),
                                  r'images\pesquia_image 2.png')
        self.image = CTkImage(light_image=Image.open(self.image), size=(550, 366))

        self.label_image = CTkLabel(self, text="", image=self.image)
        self.label_image.place(anchor=N, relx=0.322, rely=0.2)

    def config(self):
        self.limpa_janela_principal()
        self.parametros_janela_principal()
        self.title('Configurções')

        image_voltar = os.path.join(os.path.dirname(__file__),
                                    r'images\img_voltar.png')
        image_voltar = CTkImage(light_image=Image.open(image_voltar), size=(40, 40))
        self.botão_voltar = CTkButton(self, text='', image=image_voltar, width=6, fg_color='transparent',
                                      hover_color='#333', command=self.limpar_janela_config)
        self.botão_voltar.place(anchor=NE, relx=0.055, rely=0.01)

        self.frame = CTkFrame(self, width=350, height=590, corner_radius=40)
        self.frame.place(anchor=CENTER, rely=0.5, relx=0.5)

        CTkLabel(self.frame, text='Alterar/ Remover dados do banco', font=('archivo.ttf', 16)).place(
            anchor=N, relx=0.5, rely=0.07)

        option_menu = CTkOptionMenu(master=self.frame, values=['autor', 'obra', 'publicação', 'ID'], width=280,
                                    height=45, corner_radius=40, command=self.coluna)
        option_menu.place(anchor=N, rely=0.18, relx=0.5)
        option_menu.set('Escolher coluna')

        self.valor_alterado = CTkEntry(self.frame, placeholder_text='Alteração', width=280, height=45, corner_radius=40)

        self.valor_alterado.place(anchor=N, rely=0.28, relx=0.5)

        self.valor_alterado_id = CTkEntry(self.frame, placeholder_text='ID', width=280, height=45, corner_radius=40)
        self.valor_alterado_id.place(anchor=N, rely=0.38, relx=0.5)

        button = CTkButton(self.frame, text='Fazer alteração', width=280, height=45, corner_radius=40,
                           font=('archivo.ttf', 14), fg_color='green', hover_color='dark green',
                           command=self.alterar_tabela)
        button.place(anchor=CENTER, relx=0.501, rely=0.53)

        button = CTkButton(self.frame, text='Consultar tabela', width=280, height=45, corner_radius=40,
                           font=('archivo.ttf', 14), fg_color='#444', hover_color='#333', command=self.consultar_tabela)
        button.place(anchor=CENTER, relx=0.501, rely=0.63)
    def janela_cadastro_livro(self):
        self.limpa_janela_principal()
        self.parametros_janela_principal()
        self.title('Cadastro de livros')

        self.frame_livro = CTkFrame(master=self, width=330, height=590, corner_radius=40)
        self.frame_livro.place(anchor=E, rely=0.5, relx=0.995)

        self.imagem = os.path.join(os.path.dirname(__file__),
                                   r'images\img_biblioteca.png')
        self.imagem = CTkImage(light_image=Image.open(self.imagem), size=(591, 422))
        self.imagem = CTkLabel(self, text='', image=self.imagem, )
        self.imagem.place(relx=0.6, rely=0.5, anchor=E)

        img_banner = os.path.join(os.path.dirname(__file__),
                                  r'images\img_bannerbom.jpg')
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
                                   command=self.cadastro_livros)

        image_voltar = os.path.join(os.path.dirname(__file__),
                                    r'images\img_voltar.png')
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

        img_banner = os.path.join(os.path.dirname(__file__),
                                  r'images\img_bannerbom.jpg')
        img_banner = CTkImage(light_image=Image.open(img_banner), size=(330, 96))
        img_banner = CTkLabel(master=self.frame_livro, text="", image=img_banner)
        img_banner.place(relx=0.5, rely=0.18, anchor=CENTER)

        #Elementos Frame:

        self.entry = CTkEntry(self.frame_livro, placeholder_text='Livro Solicitado', width=280, height=45,
                         corner_radius=40, font=('archivo.ttf', 14))
        self.entry.place(anchor=CENTER, relx=0.501, rely=0.35)

        self.entry_id = CTkEntry(self.frame_livro, placeholder_text='ID Livro', width=280, height=45,
                            corner_radius=40, font=('archivo.ttf', 14))
        self.entry_id.place(anchor=CENTER, relx=0.501, rely=0.45)

        self.entry_senha = CTkEntry(self.frame_livro, placeholder_text='Senha Usuário', width=280, height=45,
                               corner_radius=40, font=('archivo.ttf', 14))
        self.entry_senha.place(anchor=CENTER, relx=0.501, rely=0.55)

        #Botão Empréstimo e Menu que desce:

        option_menu = CTkOptionMenu(master=self.frame_livro, values=['Prazo normal', 'Prazo extendido'], width=280, height=45,
                                    corner_radius=40)
        option_menu.place(anchor=CENTER, rely=0.65, relx=0.501)
        option_menu.set('Escolher prazo')

        button = CTkButton(self.frame_livro, text='Realizar empréstimo!', width=280, height=45, corner_radius=40,
                           font=('archivo.ttf', 14), fg_color='green', hover_color='dark green',)
        button.place(anchor=CENTER, relx=0.501, rely=0.75)

        #Botão Voltar:

        image_voltar = os.path.join(os.path.dirname(__file__),
                                    r'images\img_voltar.png')
        image_voltar = CTkImage(light_image=Image.open(image_voltar), size=(40, 40))
        self.botão_voltar = CTkButton(self, text='', image=image_voltar, width=6, fg_color='transparent',
                                      hover_color='#333',
                                      command=self.limpar_janela)
        self.botão_voltar.place(anchor=NE, relx=0.055, rely=0.01)

        #Imagem e Label:

        self.imagem = os.path.join(os.path.dirname(__file__),
                                   r'images\img_biblioteca.png')
        self.imagem = CTkImage(light_image=Image.open(self.imagem), size=(591, 422))
        self.imagem = CTkLabel(self, text='', image=self.imagem, )
        self.imagem.place(relx=0.6, rely=0.5, anchor=E)

        self.label = CTkLabel(self, text='Solicite o empréstimo do deu livro!', font=('archivo.ttf', 18))
        self.label.place(anchor=N, relx=0.325, rely=0.1)


if __name__ == "__main__":
    janela = App()
    janela.mainloop()

