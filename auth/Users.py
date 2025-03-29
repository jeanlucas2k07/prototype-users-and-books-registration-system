import sqlite3 as sq
from tkinter import messagebox
from database.DataBaseManager import DatabaseManager

class Banco(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.criar_tabela()

    def criar_tabela(self):
        query = '''
            CREATE TABLE IF NOT EXISTS acessos (
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        '''
        try:
            self._execute_query(query)
            print('Tabela criada com sucesso!')
        except RuntimeError as e:
            print(f"Erro ao criar tabela: {e}")

    def cadastro(self, email: str, senha: str) -> bool:
        self.email_cadastro = email
        self.senha_cadastro = senha

        if not self.email_cadastro or not self.senha_cadastro:
            messagebox.showinfo(title='Login', message='Preencha todos os campos!')
            return False

        if len(self.senha_cadastro) <= 5:
            messagebox.showinfo(title='Login', message='A senha deve ter mais de cinco caracteres.')
            return False

        query = "INSERT INTO acessos (email, senha) VALUES (?, ?)"
        params = (self.email_cadastro, self.senha_cadastro)

        try:
            self._execute_query(query, params)
            messagebox.showinfo(title='Login', message='Cadastro efetuado com sucesso!\nVolte à tela de login para efetuá-lo')
            return
        
        except RuntimeError as e:
            messagebox.showerror(title='Erro', message=f'Erro ao cadastrar: {e}')
            return False

    def login(self, email: str, senha: str) -> bool:
        self.email_log = email
        self.senha_log = senha

        query = "SELECT * FROM acessos WHERE email = ? AND senha = ?"
        params = (self.email_log, self.senha_log)

        try:
            resultado = self._fetch_query(query, params)
            if resultado:
                return True
            else:
                messagebox.showinfo(title='Login', message='Credenciais inválidas. Tente novamente.')
                return False
            
        except RuntimeError as e:
            messagebox.showerror(title='Erro', message=f'Erro ao realizar login: {e}')
            return False