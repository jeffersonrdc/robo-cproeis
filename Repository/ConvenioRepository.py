from Repository.conexao_mysql import ConexaoMySQL


class ConvenioRepository:
    def __init__(self):
        self.conexao = ConexaoMySQL()
        self.conexao.conectar()