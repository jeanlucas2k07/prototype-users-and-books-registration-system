from .google_books_api import Livros
from utils.p import LivroFrame

class Busca(LivroFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.livros_api = Livros()
        self.grid(row=1, column=1, sticky="")
    
    def buscar(self, busca: str):
        if hasattr(self, "bestsellers"):
            self.bestsellers.grid_forget()
        
        livros_encontrados = self.livros_api.buscaISBN(busca)
        self.exibir_livros(livros_encontrados)

        if busca == "":
            self.exibir_bestsallers()
