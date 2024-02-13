import bcrypt

def criptografarSenha(senha):
    # Gerar um salt aleatório
    salt = bcrypt.gensalt()

    # Criptografar a senha usando o salt
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), salt)

    return senha_criptografada

def descriptografarSenha(senha_digitada, senha_criptografada):
    # Verificar se a senha digitada corresponde à senha criptografada
    return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_criptografada)
