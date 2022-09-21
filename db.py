import mysql.connector
from mysql.connector import errorcode
from Usuarie import *

#!#! TODO: Descobrir como adicionar/atualizar mais de um registro por vez no MySQL.

def conectar_bd():
	try:
		conexao_bd = mysql.connector.connect(host='162.214.166.89', user='lauramadel', password='7he2ya984bcl', database='amizades')
		print("Banco de dados conectado!")
	except mysql.connector.Error as error:
		if error.errno == errorcode.ER_BAD_DB_ERROR:
			print("Banco de Dados não existe!")
		elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Nome de suárie ou senha incorretes")
		else:
			print(error)
		return

	return conexao_bd

def desconectar_bd(conexao_bd):
	conexao_bd.commit()
	conexao_bd.close()
	print("Banco de dados desconectado!")

# TODO: Continuar testes no BD
# TODO: Falhas: pronomes depois de pular linha; n-b, b/b
# TODO: fracionar função
def escreve_sql_select_usuaries(variaveis, interesses, proibidos, pronomes):

	interesses_aux = []
	proibidos_aux = []
	pronomes_aux = []

	sql = "SELECT " + ', '.join(variaveis) + " FROM usuaries WHERE "

	if proibidos:
		for proibido in proibidos:
			proibidos_aux.append("nome NOT LIKE '%" + proibido + "%' AND bio NOT LIKE '%" + proibido + "%'")

		sql += ' AND '.join(proibidos_aux) + " AND ("

	for interesse in interesses:
		interesses_aux.append("nome LIKE '%" + interesse + "%' OR bio LIKE '%" + interesse + "%'")

	sql += ' OR '.join(interesses_aux)

	if pronomes:
		for pronome in pronomes:
			pronomes_aux.append("bio REGEXP '[0-9🏳️‍⚧️\
 °:(){}&.,?!''/|<>-]" + pronome + "' OR bio REGEXP '^" + pronome + "' OR nome REGEXP '[0-9🏳️‍⚧️\
 °:(){}&.,?!''/|<>-]" + pronome + "'")
		sql += " OR " + ' OR '.join(pronomes_aux)

	if proibidos:
		sql += ")"

	sql += ";"

	# Limpa, limpa, limpa
	variaveis.clear()
	proibidos.clear()
	interesses.clear()
	pronomes.clear()
	proibidos_aux.clear()
	interesses_aux.clear()
	pronomes_aux.clear()

	print(sql)
	return sql

def baixa_usuaries_bd(conexao_bd):
	cursor = conexao_bd.cursor()
	usuaries : Usuarie = []

	variaveis = ["id", "nome", "bio", "arroba", "eu_sigo", "cont_seguidores", "cont_seguides", "protegide", "local", "url"]
	interesses = ["🌈", "⚧", "gênero", "nb", "pronome", "UFPR", "trans", "travest", "trava", "ativista", "LGBT"]
	pronomes = ["ela", "ele", "elu"]
	proibidos = ["🔞", "😈", "NSFW", "sex", "only", "📚", "📖", "book", "otak", "anime", "fandom", "game", "play", "🎮", "jog"]

	cursor.execute(escreve_sql_select_usuaries(variaveis, interesses, proibidos, pronomes))
	print(0)
	resultado = cursor.fetchall()
	print(1)
	for usuarie in resultado:
		usuaries.append(Usuarie(id=usuarie[0],
								nome=usuarie[1],
								bio=usuarie[2],
								arroba=usuarie[3],
								eu_sigo=usuarie[4],
								cont_seguidores=usuarie[5],
								cont_seguides=usuarie[6],
								protegide=usuarie[7],
								local=usuarie[8],
								url=usuarie[9]))
	cursor.close()
	print(2)
	return usuaries

def escreve_sql_insert_usuarie():
	sql = "INSERT INTO usuaries (id, nome, arroba, bio, me_segue, eu_sigo, cont_seguidores, cont_seguides, foto, protegide, local, url, verificade, inseride_quando) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()) " \
			  "ON DUPLICATE KEY UPDATE nome=%s, arroba=%s, bio=%s, me_segue=%s, eu_sigo=%s, cont_seguidores=%s, cont_seguides=%s, foto=%s, protegide=%s, local=%s, url=%s, verificade=%s, atualizade_quando=NOW()"
	return sql
def escreve_porcento_s(quantidade):
    s = []
    for i in range(0, quantidade, 1):
        s.append("%s")
    return ', '.join(s)

def escreve_sql_insert_usuarie(variaveis, variaveis_atualizar):
	sql = "INSERT INTO usuaries (" + ', '.join(variaveis) + ", inseride_quando) VALUES (" + escreve_porcento_s(len(variaveis)) + ", NOW()) ON DUPLICATE KEY UPDATE " + '=%s, '.join(variaveis_atualizar) + "=%s, atualizade_quando=NOW()"
	return sql

# TODO absurdo: me segue/eu sigo são opostos dicotomicos!! Verificar se já existe um valor antes de alterar
# TODO: essa funçao só pega um por vez mesmo? pra que o for?
def adiciona_usuarie_bd(usuaries, conexao_bd):

	cursor = conexao_bd.cursor()


	for usuarie in usuaries:

		variaveis = ["id",
					 "nome",
					 "arroba",
					 "bio",
					 "cont_seguidores",
					 "cont_seguides",
					 "foto",
					 "protegide",
					 "local",
					 "url",
					 "verificade"]

		variaveis_atualizar = ["nome",
							   "arroba",
							   "bio",
							   "cont_seguidores",
							   "cont_seguides",
							   "foto",
							   "protegide",
							   "local",
							   "url",
							   "verificade"]

		valores = (usuarie.id,
				  usuarie.nome,
				  usuarie.arroba,
				  usuarie.bio,
				  usuarie.cont_seguidores,
				  usuarie.cont_seguides,
				  usuarie.foto,
				  usuarie.protegide,
				  usuarie.local,
				  usuarie.url,
				  usuarie.verificade)

		valores_atualizar = (usuarie.nome,
							 usuarie.arroba,
							 usuarie.bio,
							 usuarie.cont_seguidores,
							 usuarie.cont_seguides,
							 usuarie.foto,
							 usuarie.protegide,
							 usuarie.local,
							 usuarie.url,
							 usuarie.verificade)

		if usuarie.me_segue == True:
			variaveis.append("me_segue")
			variaveis_atualizar.append("me_segue")
			valores += (usuarie.me_segue,)
			valores_atualizar += (usuarie.me_segue,)
		if usuarie.eu_sigo == True:
			variaveis.append("eu_sigo")
			variaveis_atualizar.append("eu_sigo")
			valores += (usuarie.eu_sigo,)
			valores_atualizar += (usuarie.eu_sigo,)

		sql = escreve_sql_insert_usuarie(variaveis, variaveis_atualizar)

		values = (usuarie.id,
				  usuarie.nome,
				  usuarie.arroba,
				  usuarie.bio,
				  usuarie.cont_seguidores,
				  usuarie.cont_seguides,
				  usuarie.foto,
				  usuarie.protegide,
				  usuarie.local,
				  usuarie.url,
				  usuarie.verificade,
				  usuarie.me_segue,
				  usuarie.eu_sigo,
				  # ATUALIZA:
				  usuarie.nome,
				  usuarie.arroba,
				  usuarie.bio,
				  usuarie.cont_seguidores,
				  usuarie.cont_seguides,
				  usuarie.foto,
				  usuarie.protegide,
				  usuarie.local,
				  usuarie.url,
				  usuarie.verificade,
				  usuarie.me_segue,
				  usuarie.eu_sigo)

		cursor.execute(sql, valores + valores_atualizar)

		if(cursor.rowcount == 0):
			print("ERRO NA INSERÇÃO!!!")
			# atualiza_usuaries_bd([usuarie], conexao_bd)
		else:
			print("o registro de < " + usuarie.nome + " > foi inserido.")

		variaveis.clear()
		variaveis_atualizar.clear()
	cursor.close()

# def atualiza_usuaries_bd(usuaries, conexao_bd):
# 	cursor = conexao_bd.cursor()
# 	for usuarie in usuaries:
# 		# Se a bio for apagada, não atualiza ela.
# 		if(usuarie.bio != ""):
# 			sql = ("update usuaries set bio = %s, nome = %s, arroba = %s, me_segue = %s, eu_sigo = %s, cont_seguidores = %s, cont_seguides = %s, foto = %s, protegide = %s, atualizade_quando = NOW() where id=%s")
# 			values = (usuarie.bio, usuarie.nome, usuarie.arroba, usuarie.me_segue, usuarie.eu_sigo, usuarie.cont_seguidores, usuarie.cont_seguides, usuarie.foto, usuarie.protegide, usuarie.id)
# 		else:
# 			sql = ("update usuaries set nome = %s, arroba = %s, me_segue = %s, eu_sigo = %s, cont_seguidores = %s, cont_seguides = %s, foto = %s, atualizade_quando = NOW() where id=%s")
# 			values = (usuarie.nome, usuarie.arroba, usuarie.me_segue, usuarie.eu_sigo, usuarie.cont_seguidores, usuarie.cont_seguides, usuarie.foto, usuarie.id)
# 		cursor.execute(sql, values)
# 		print("as infos de < "+ usuarie.nome +" > foram atualizadas.")
# 	# if cursor.rowcount != 0:
# 	# 	print(str(cursor.rowcount) + " registros foram atualizados.")
#
# 	cursor.close()