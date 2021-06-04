def conversion(token):
    token = token.split()[0]
    token = token.encode()
    token = token.decode()
    return token
