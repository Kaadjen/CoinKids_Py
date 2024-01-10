import hashlib

"""
Ce fichier comporte une unique classe nommée DoubleHashing.
"""

class DoubleHashing:
    """
    Cette classe est composée de trois méthodes statiques :
        -_hash1
        -_hash2
        -double_hash
    """

    def __init__(self):
        """
        Aucun objet de type DoubleHashing n'a besoin d'être initialisé.
        """
        pass

    @staticmethod
    def _hash1(key):
        """
        Cette méthode va permettre de hasher une chaine de caractère à l'aide de sha224.
        :param key: chaine de caractère
        :return: hash valeur
        """
        # SHA-224
        hash_object = hashlib.sha224(key.encode())
        return hash_object.hexdigest()

    @staticmethod
    def _hash2(key):
        """
        Cette méthode va permettre de hasher une chaine de caractère à l'aide de sha256.
        :param key: chaine de caractère
        :return:  hash valeur
        """
        # SHA-256
        hash_object = hashlib.sha256(key.encode())
        return hash_object.hexdigest()

    @staticmethod
    def double_hash(key):
        """
        Cette méthode va permettre d'effectuer un double hash sur une chaine de caractère.
        :param key: chaine de caractère
        :return: double hash valeur
        """
        hash1 = DoubleHashing._hash1(key)
        hash = DoubleHashing._hash2(hash1)
        return hash


'''key = "***"
result = DoubleHashing.double_hash(key)
print("Hash:", result)'''
