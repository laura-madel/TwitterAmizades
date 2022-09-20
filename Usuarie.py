class Usuarie:
    def __init__(self, id="", nome="", arroba="", bio="", me_segue=False, eu_sigo=False, cont_seguidores=0, cont_seguides=0, foto="", protegide=False, local="", url="", verificade=False):
        self.id = id
        self.nome = nome
        # TODO: refatorar para arroba
        self.arroba = arroba
        self.bio = bio
        self.me_segue = me_segue
        self.eu_sigo = eu_sigo
        self.cont_seguidores = cont_seguidores
        self.cont_seguides = cont_seguides
        self.foto = foto
        self.protegide = protegide
        self.local = local
        self.url = url
        self.verificade = verificade
class Pontuacao:
    def __init__(self, usuarie:Usuarie, pontos=0, coerencia = 0, porn = False):
        self.usuarie = usuarie
        self.pontos = pontos
        self.coerencia = coerencia
        self.porn = porn

    def __lt__(self, other):
        if self.pontos == other.pontos:
            return self.coerencia < other.coerencia
        return self.pontos < other.pontos