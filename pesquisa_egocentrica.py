def adiciona_tags(usuaries, tag):

    if tag == "marcar_como_seguide":
        for usuarie in usuaries:
            usuarie.eu_sigo = True

    if tag == "marcar_como_seguidor":
        for usuarie in usuaries:
            usuarie.me_segue = True

    return usuaries