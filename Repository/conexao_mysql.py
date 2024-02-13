import mysql.connector


class ConexaoMySQL:
    def __init__(self):
        self.conexao = None

    def conectar(self):
        # Substitua 'seu_usuario', 'sua_senha' e 'seu_banco_de_dados' com suas credenciais
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="roboproeis"
        )

        return self.conexao

    def fecharConexao(self):
        if self.conexao:
            self.conexao.close()
            self.conexao = None
