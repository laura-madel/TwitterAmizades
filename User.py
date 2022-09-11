class User:
    def __init__(self, id="", nome="", username="", bio="", me_segue=False, eu_sigo=False, cont_seguidores=0,cont_seguidos=0,foto=""):
        self.id = id
        self.nome = nome
        self.username = username
        self.bio = bio
        self.me_segue = me_segue
        self.eu_sigo = eu_sigo
        self.cont_seguidores = cont_seguidores
        self.cont_seguidos = cont_seguidos
        self.foto = foto