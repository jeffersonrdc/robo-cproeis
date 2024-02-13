from Repository.conexao_mysql import ConexaoMySQL
from Service.UtilService import criptografarSenha


class LoginRepository:
    def __init__(self):
        self.conexao = ConexaoMySQL()
        self.conexao.conectar()

    def salvarLogin(self, ID_TipoLogin, NM_Usuario, NM_Senha):
        try:
            # Comando SQL para realizar o INSERT
            sql_insert = "INSERT INTO login (ID_TipoLogin, NM_Usuario, NM_Senha) VALUES (%s, %s, %s)"
            # Valores a serem inseridos
            valores = (ID_TipoLogin, NM_Usuario, criptografarSenha(NM_Senha))
            cursor = self.conexao.conexao.cursor()
            cursor.execute(sql_insert, valores)
            # Commit para efetivar a transação no banco de dados
            self.conexao.conexao.commit()

            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()
            # Não se esqueça de fechar a conexão quando terminar
            self.conexao.fecharConexao()

        return 0
