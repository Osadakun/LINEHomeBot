def conversion(token):
    token = token.split()[0]
    token = token.encode()
    token = token.decode()
    return token

def bsend(token):
    token = token.replace('[','')
    token = token.replace('(','',4)
    token = token.replace('),','\n')
    token = token.replace("'",'',16)
    token = token.replace(']','')
    return token
