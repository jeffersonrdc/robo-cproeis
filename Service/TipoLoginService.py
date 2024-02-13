from Repository.TipoLoginRepository import *


def retornaTipoLogin():
    repository = TipoLoginRepository()

    # Chame a função retorna_tipo_login
    resultados = repository.retornaTipoLogin()

    return resultados