from database.DataBaseManager import DatabaseManager
import pickle

class LivrosSalvos(DatabaseManager):
    def __init__(self, id_user: int):
        super().__init__()
        self._execute_query("""CREATE TABLE IF NOT EXISTS livros_salvos (livro BLOB, id INTEGER PRIMARY KEY AUTOINCREMENT, id_user INTEGER, FOREIGN KEY (id_user) REFERENCES acessos(id) ON DELETE CASCADE)""")
        self.id_user = id_user

    def AdicionarLivros(self, livro):
        self.livro = pickle.dumps(livro)
        self._execute_query("""INSERT INTO livros_salvos (livro, id_user)VALUES (?, ?)""", (self.livro, self.id_user))
        print(self.id_user)
        

