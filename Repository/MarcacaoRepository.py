from Repository.conexao_mysql import ConexaoMySQL


class MarcacaoRepository:
    def __init__(self):
        self.conexao = ConexaoMySQL()
        self.conexao.conectar()