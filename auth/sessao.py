class Sessao:
    _id_usuario = None

    @classmethod
    def salvar_id(cls, id_user):
        cls._id_usuario = id_user
    
    @classmethod
    def return_id(cls):
        return cls._id_usuario
    
    def limpar_sessao(cls):
        cls._id_usuario = None