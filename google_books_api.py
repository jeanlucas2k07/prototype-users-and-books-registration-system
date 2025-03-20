import requests
import tkinter as tk
from tkinter import filedialog
from bancoImagens import Images

class Livros:
    @staticmethod
    def __busca(url: str) -> list[dict[str, str]]:
        livros = list()
        response = requests.get(url)
        data = response.json()

        if "items" in data:
            for item in data["items"]:
                book = item["volumeInfo"]
                titulo = book.get("title", "Título não encontrado")
                autores = ", ".join(book.get("authors", ["Autor desconhecido"]))
                descricao = book.get("description", "Sem descrião disponível")
                capa = book.get("imageLinks", {}).get("thumbnail", "Sem capa")
                identificador = book.get("industryIdentifiers")
                if len(identificador) > 1:
                    isbn = identificador[1]["identifier"]
                else:
                    isbn = identificador[0]["identifier"] if identificador else "ISBN não disponível"

                livros.append({
                    "titulo": titulo,
                    "autores": autores,
                    "descricao": descricao,
                    "capa": capa,
                    "ISBN": isbn
                })

            return livros
        
        else: return []

    def buscaISBN(self, isbn: str) -> list[dict[str, str]]:
        return self.__busca(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")

    def buscaTitulo(self, titulo: str) -> list[dict[str, str]]:
        return self.__busca(f"https://www.googleapis.com/books/v1/volumes?q={titulo}")
    
    def buscarBestsellers(self) -> list[dict[str, str]]:
        return self.__busca(f"https://www.googleapis.com/books/v1/volumes?q=bestseller")

# l = Livros()
# i = Images()

# ISBN = input("Digite o ISBN: ")
# retorno = l.buscaTitulo("Dexter")

# if retorno[0]["capa"] == "Sem capa":
#     img = i.checarImagem(ISBN)

#     if img == False:
#         colocarCapa = input("Quer adicionar uma capa? (S/n)").lower()

#         if colocarCapa == "s":

#             root = tk.Tk()
#             root.withdraw()

#             capa = filedialog.askopenfilename(title='Selecione a capa do livro', filetypes=[("Imagens", "*.png; *.jpg; *.jpeg; *.gif")])

#             if capa:
#                 print(f"Imagem selecionada: {capa}")
#             else:
#                 print("Nenhuma imagem foi selecionada.")

#             if capa:
#                 with open(capa, "rb") as img:
#                     blobImage = img.read()
#                     if "-" in ISBN:
#                         ISBN = ISBN.replace("-", "")
#                     i.adicionarValores(blobImage, ISBN)
