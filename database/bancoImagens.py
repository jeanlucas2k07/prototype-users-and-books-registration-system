from database.DataBaseManager import DatabaseManager
from typing import Union
import sqlite3 as sq

class Images(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.__criar_tabela()
    
    def __criar_tabela(self) -> sq.Connection:
        query = """CREATE TABLE IF NOT EXISTS livrosImages(isbn TEXT NOT NULL, image BLOB NOT NULL)"""
        return self._execute_query(query)
    
    def adicionarValores(self, image: bytes, isbn: str) -> sq.Connection:
        query = """INSERT INTO livrosImages (isbn, image) VALUES (?, ?)"""
        return self._execute_query(query, (isbn, image))

    def checarImagem(self, isbn: str) -> Union[bytes, bool]:
        query = '''SELECT image FROM livrosImages WHERE isbn = ?'''
        image = self._fetch_query(query, (isbn,))

        if image:
            return image[0][0]
        
        return False
    
    def deletarImagem(self, isbn: str) -> sq.Connection:
        query = "DELETE FROM livrosImages WHERE isbn = ?"
        return self._execute_query(query, (isbn,))

