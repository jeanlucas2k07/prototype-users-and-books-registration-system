import sqlite3 as sq
import os

class DatabaseManager:
    def __init__(self) -> None:
        self.db_dir = 'data'
        self.db_name = 'database.db'
        self.db_path = os.path.join(self.db_dir, self.db_name)
        os.makedirs(self.db_dir, exist_ok=True)
    
    def _connect(self) -> sq.Connection:
        return sq.connect(self.db_path)
    
    def _execute_query(self, query: str, params: tuple = ()) -> None:
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
        except sq.Error as e:
            raise RuntimeError(f"Erro no banco de dados: {e}")
    
    def _fetch_query(self, query: str, params: tuple = ()):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                return cursor.execute(query, params).fetchall()
        except sq.Error as e:
            raise RuntimeError(f"Erro no banco de dados: {e}")
        