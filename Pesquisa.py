import tkinter as tk
from DataBaseManager import DatabaseManager
from tkinter import messagebox, scrolledtext

class Pesquisa(DatabaseManager):
    def __init__(self):
        super().__init__()

    def buscar_livro(self, termo_pesquisa: str) -> None:
        query = "SELECT * FROM livros WHERE LOWER(obra) LIKE ?"
        resultado = self._fetch_query(query, (f"%{termo_pesquisa.lower()}%",))

        if resultado:
            self._exibir_resultados('Resultados da busca:', resultado)
        else:
            messagebox.showinfo(title='Busca de livros', message="Infelizmente, não temos este livro.")

    def busca_detalhada(self, termo_pesquisa: str, metodo: str) -> None:
        if metodo == 'ID':
            query = "SELECT * FROM livros WHERE ID = ?"
        else:
            query = f"SELECT * FROM livros WHERE {metodo} LIKE ?"

        resultado = self._fetch_query(query, (f"%{termo_pesquisa}%",))

        if resultado:
            self._exibir_resultados(f'Resultados encontrados ({metodo}):', resultado)
        else:
            messagebox.showinfo(title='Busca detalhada', message='Nenhum resultado encontrado.')

    def PesquisarPorAutor(self, autor: str):
        if not isinstance(autor, str) or not autor.strip():
            messagebox.showerror("Erro", "Informe um autor válido!")
            return

        query = "SELECT * FROM livros WHERE autor LIKE ?"
        valores = self._fetch_query(query, (f"%{autor}%",))

        self._exibir_resultados(valores, f"Pesquisa por Autor: {autor}")

    def PesquisarPorObra(self, obra: str):
        if not isinstance(obra, str) or not obra.strip():
            messagebox.showerror("Erro", "Informe uma obra válida!")
            return

        query = "SELECT * FROM livros WHERE obra LIKE ?"
        valores = self._fetch_query(query, (f"%{obra}%",))

        self._exibir_resultados(valores, f"Pesquisa por Obra: {obra}")

    def PesquisarPorID(self, livro_id: int):
        if not isinstance(livro_id, int):
            messagebox.showerror("Erro", "O ID deve ser um número inteiro válido!")
            return

        query = "SELECT * FROM livros WHERE id = ?"
        valores = self._fetch_query(query, (livro_id,))

        self._exibir_resultados(valores, f"Pesquisa por ID: {livro_id}")

    def _exibir_resultados(self, valores, titulo):
        if not valores:
            messagebox.showinfo("Resultado", "Nenhum livro encontrado!")
            return

        janela_resultado = tk.Toplevel()
        janela_resultado.title(titulo)

        text_resultado = scrolledtext.ScrolledText(janela_resultado, wrap=tk.WORD, width=80, height=20)
        text_resultado.pack(padx=10, pady=10)

        text_resultado.insert(tk.END, f"{titulo}\n")
        text_resultado.insert(tk.END, "-" * 80 + "\n")

        for valor in valores:
            text_resultado.insert(tk.END, f"Livro: {valor[1]}\nAutor: {valor[0]}\nAno: {valor[3]}\nID: {valor[2]}\n\n")

        text_resultado.config(state=tk.DISABLED)

