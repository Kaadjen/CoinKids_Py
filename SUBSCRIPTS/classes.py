import json, os

"""
Ce fichier contient trois classes :
    -Parents
    -Enfants 
    -Histofiles
"""

class Parents:
    """
    Cette classe permet de créer un objet de type Parents.
    """
    def __init__(self, username, passwd):
        """
        Cette méthode initialise les attributs d'un objet de type Parents.
        :param username: nom de l'utilisateur
        :param passwd: mot de passe de l'utilisateur
        """
        self.username = username
        self.passwd = passwd


class Enfants:
    """
    Cette classe permet de créer un objet de type Enfants.
    """
    def __init__(self, id_parent, nom, genre, montant_depart, porte_monnaie, montant_dajout, frequence, horloge, compte_bancaire, compte_paypal):
        """
        Cette méthode permet d'initialiser les attributs d'un objet Enfants.
        :param id_parent: nom de l'utilisateur avec lequel l'objet est créé
        :param nom: nom de l'enfant
        :param genre: genre de l'enfant
        :param montant_depart: montant attribué initialement au compte de l'enfant
        :param porte_monnaie: solde de l'enfant
        :param montant_dajout: somme d'argent de poche de l'enfant
        :param frequence: fréquence à laquelle l'argent de poche est versé à l'enfant
        :param horloge: date et heure de création d'un profil enfant
        :param compte_bancaire: compte bancaire de l'enfant
        :param compte_paypal: compte paypal de l'enfant
        """
        self.id_parent = id_parent
        self.nom = nom
        self.genre = genre
        self.montant_depart = montant_depart
        self.porte_monnaie = porte_monnaie
        self.montant_dajout = montant_dajout
        self.frequence = frequence
        self.horloge = horloge
        self.compte_bancaire = compte_bancaire
        self.compte_paypal = compte_paypal




class HistoFiles:
    """
    Cette classe permet d'effectuer de la lecture et de l'écriture sur un fichier historique.
    """
    def __init__(self, gid):
        """
        Cette méthode permet d'initialiser la position du fichier de sauvegarde de l'historique d'un enfant donné.
        :param gid: global_id de la table enfants
        """
        self.gid = gid
        self.file = str("./history/"+str(gid) + ".txt")
        self.data = []

    def get_files(self):
        """
        Cette méthode renvoie les différentes transactions d'un fichier de sauvegarde de l'historique.
        Si aucun fichier de sauvegarde de l'historique n'est trouvé, alors il est créé.
        :return: les transactions d'un profil enfant
        """
        if not os.path.exists(self.file):
            with open(self.file, 'w') as fichier:
                donnees_json = json.dumps("", ensure_ascii=False)
                fichier.write(donnees_json + '\n')
        with open(self.file, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                donnees_dict = json.loads(ligne.strip())
                self.data.append(donnees_dict)
        return self.data

    def push_files(self, icone, type, montant):
        """
        Cette méthode va permettre d'ajouter une transaction au fichier de l'historique.
        :param icone: image du type de transaction
        :param type: BANK/PAYPAL/CASH : pour les retraits; AJOUT : pour ajouts et virements
        :param montant: somme de la transaction
        :return: None
        """
        donnees = {
            'icon': icone,
            'type': type,
            'amount': montant
        }
        donnees_json = json.dumps(donnees, ensure_ascii=False)

        with open(self.file, 'a', encoding='utf-8') as fichier:
            fichier.write(donnees_json + '\n')
