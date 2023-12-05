from hashlib import sha3_256
import logging

class Funcoes(object):
    
    @staticmethod
    def cifraSenha(senha):
        hashed_password = sha3_256(senha.encode('utf-8')).hexdigest()
        logging.debug(f"Senha cifrada: {hashed_password}")
        return hashed_password