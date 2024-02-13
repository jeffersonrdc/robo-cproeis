from Repository.conexao_mysql import ConexaoMySQL


class TipoLoginRepository:
    def __init__(self):
        self.conexao = ConexaoMySQL()
        self.conexao.conectar()

    def retornaTipoLogin(self):
        try:
            cursor = self.conexao.conexao.cursor()
            cursor.execute("SELECT ID_TipoLogin, NM_TipoLogin FROM tipo_login WHERE IS_Ativo = true")
            resultados = cursor.fetchall()

            return resultados
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            # Não se esqueça de fechar a conexão quando terminar
            self.conexao.fecharConexao()
