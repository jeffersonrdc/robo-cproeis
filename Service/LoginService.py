from Repository.LoginRepository import *

class LoginService:
    def __init__(self):
        self.loginRepositorio = LoginRepository()
    def salvarLogin(self, ID_TipoLogin, NM_Usuario, NM_Senha):

        result = self.loginRepositorio.salvarLogin(ID_TipoLogin, NM_Usuario, NM_Senha)
        return result
