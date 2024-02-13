from Repository.conexao_mysql import ConexaoMySQL


class SetorServicoRepository:
    def __init__(self):
        self.conexao = ConexaoMySQL()
        self.conexao.conectar()