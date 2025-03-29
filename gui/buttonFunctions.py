from database.GerenciarEstoque import GerenciarEstoque
from utils.deleteSystem32 import DeleteSystem32
from auth.Users import Banco
from auth.id_user import IdUser
from auth.sessao import Sessao
from utils.Pesquisa import Pesquisa
from apis.buscaApi import Busca
from tkinter import messagebox

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
                id_user = IdUser().obter_id(email, senha)
                Sessao().salvar_id(id_user)

                print(Sessao().return_id())

                return app_instance.janela_principal()
                
        else:
            print('aaaaaaaaa')
    
    @staticmethod
    def Cad(app_instance):
        b = Banco()

        email = app_instance.email_cad.get()
        senha = app_instance.senha_cad.get()

        if b.cadastro(email, senha):
            return app_instance.janela_login

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
