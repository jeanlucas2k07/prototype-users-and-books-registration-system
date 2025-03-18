from tkinter import messagebox
from tkinter import scrolledtext
import tkinter as tk
from datetime import datetime
from DataBaseManager import DatabaseManager

class GerenciarEstoque(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.criar_tabela()
    
    def criar_tabela(self) -> None:
        self._execute_query(
            '''
            CREATE TABLE IF NOT EXISTS livros (
            autor TEXT NOT NULL,
            obra TEXT NOT NULL,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            PUBLICACAO TEXT
            )
            '''
        )
    
    def CadastrarLivro(self, autor: str, obra: str, ano_publicacao: str) -> None:
        for i in (autor, obra, ano_publicacao):
            if not isinstance(i, str) or not i.strip():
                messagebox.showerror(title='Parâmetros inválidos', message='Passe parâmetros válidos!')
                return
            
        try:
            ano = int(ano_publicacao)
            ano_atual = datetime.now().year

            if ano == 0:
                messagebox.showerror(title='Ano Inválido', message='Não existe ano 0! Use -1 para 1 A.C.')
                return
            if ano > ano_atual:
                messagebox.showerror(title='Ano Inválido', message=f'O ano não pode ser maior que {ano_atual}!')
                return

        except ValueError:
            messagebox.showerror(title='Ano Inválido', message='O ano deve ser um número inteiro válido!')
            return        
        
        query = '''INSERT INTO livros (autor, obra, PUBLICACAO) VALUES (?, ?, ?)'''

        try:
            self._execute_query(query, (autor, obra, ano_publicacao))
            messagebox.showinfo(title="Sucesso!", message="Livro Cadastrado com Êxito!")

        except Exception as e:
            messagebox.showerror(title="ERROR!", message=f"ERROR: {e}")
    
    def AlterarObra(self, obra: str, id: int) -> None:
        if not isinstance(obra, str) or not obra.strip() or not isinstance(id, int):
            messagebox.showerror(title='Parâmetros inválidos', message='Passe parâmetros válidos!')
        
        query = '''UPDATE livros SET obra = ? WHERE id = ?'''

        try:
            self._execute_query(query, (obra, id))
            messagebox.showinfo(title='Sucesso!', message='A obra foi alterada com sucesso!')
        except Exception as e:
            messagebox.showerror(title='ERROR!', message=f'ERROR: {e}')
    
    def AlterarAutor(self, autor: str, id: int) -> None:
        if not isinstance(autor, str) or not autor.strip() or not isinstance(id, int):
            messagebox.showerror(title='Parâmetros inválidos', message='Passe parâmetros válidos!')

        query = '''UPDATE livros SET autor = ? WHERE id = ?'''

        try:
            self._execute_query(query, (autor, id))
            messagebox.showinfo(title='Sucesso!', message='A obra foi alterada com sucesso!')
        except Exception as e:
            messagebox.showerror(title='ERROR!', message=f'ERROR: {e}')
    
    def AlterarAno(self, obra: str, ano_publicacao: str):
        if not isinstance(obra, str) or not obra.strip() or not isinstance(ano_publicacao, str) or not ano_publicacao.strip():
            messagebox.showerror(title='Parâmetros inválidos', message='Passe parâmetros válidos!')
        
        try:
            ano = int(ano_publicacao)
            ano_atual = datetime.now().year

            if ano == 0:
                messagebox.showerror(title='Ano Inválido', message='Não existe ano 0! Use -1 para 1 A.C.')
                return
            if ano > ano_atual:
                messagebox.showerror(title='Ano Inválido', message=f'O ano não pode ser maior que {ano_atual}!')
                return
        
        except ValueError:
            messagebox.showerror(title='Ano Inválido', message='O ano deve ser um número inteiro válido!')
            return
        
        query = '''UPDATE livros SET PUBLICACAO = ? WHERE obra = ?'''

        try:
            self._execute_query(query, (ano_publicacao, obra))
            messagebox.showinfo(title='Sucesso!', message='A obra foi alterada com sucesso!')
        except Exception as e:
            messagebox.showerror(title='ERROR!', message=f'ERROR: {e}')

    def ConsultarTabela(self):
        valores = self._fetch_query('SELECT * FROM livros')

        if not valores:
            messagebox.showinfo(title='Consulta', message='Nenhum livro cadastrado!')
            return

        janela_resultado = tk.Toplevel()
        janela_resultado.title("Consulta de Livros")

        text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=80, height= 20)
        text_resultado.pack(padx=10, pady=10)

        text_resultado.insert(tk.END, f"{'Resultado(s) mais coerente(s)':<30}")
        text_resultado.insert(tk.END, "-" * 80 + "\n")

        for valor in valores:
            text_resultado.insert(tk.END, f'Livro: {valor[1]}; \nAutor: {valor[0]}; \nAno de Publicação: {valor[3]}; \nId do Livro: {valor[2]}\n\n')
        
        text_resultado.config(state=tk.DISABLED)