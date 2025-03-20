import requests

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

                livros.append({
                    "titulo": titulo,
                    "autores": autores,
                    "descricao": descricao,
                    "capa": capa
                })

            return livros
        
        else: return []

    def buscaISBN(self, isbn: str) -> list[dict[str, str]]:
        return self.__busca(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")

    def buscaTitulo(self, titulo: str) -> list[dict[str, str]]:
        return self.__busca(f"https://www.googleapis.com/books/v1/volumes?q={titulo}")
    
    def buscarBestsellers(self) -> list[dict[str, str]]:
        return self.__busca(f"https://www.googleapis.com/books/v1/volumes?q=bestseller")

