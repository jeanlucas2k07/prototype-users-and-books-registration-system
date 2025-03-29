from database.DataBaseManager import DatabaseManager

class IdUser:
    def __init__(self):
        self.id_user = None  # Armazena o ID do usuário
        

    def obter_id(self, user, senha):
        id_usuario = self.buscar_id_usuario(user, senha)
        if id_usuario:
            self.id_user = id_usuario  # Armazena o ID
        return id_usuario

    def buscar_id_usuario(self, user, senha):
        resultado = DatabaseManager()._fetch_query("""SELECT id FROM ACESSOS WHERE email = ? and senha = ?""", (user, senha))
        if resultado:
            return resultado[0][0]
        else:
            return None