from Repository.conexao_mysql import ConexaoMySQL


class UnidadeRepository:
    def __init__(self):
        self.conexao = ConexaoMySQL()
        self.conexao.conectar()