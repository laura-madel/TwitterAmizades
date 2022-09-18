import mysql.connector
from mysql.connector import errorcode
from User import *

#!#! TODO: Descobrir como adicionar/atualizar mais de um registro por vez no MySQL.

def conectar_bd():
	try:
		db_connection = mysql.connector.connect(host='162.214.166.89', user='lauramadel', password='7he2ya984bcl', database='amizades')
		print("Banco de dados conectado!")
	except mysql.connector.Error as error:
		if error.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database doesn't exist")
		elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("User name or password is wrong")
		else:
			print(error)
		return

	return db_connection

def desconectar_bd(db_connection):
	db_connection.commit()
	db_connection.close()
	print("Banco de dados desconectado!")

def baixa_user_bd(db_connection):
	cursor = db_connection.cursor()
	users : User = []
	# TODO: Adicionar outros interesses
	sql = "SELECT id, nome, bio, username, eu_sigo, cont_seguidores, cont_seguidos, fechado FROM users WHERE bio NOT LIKE '%🔞%' AND nome NOT LIKE '%🔞%' AND (nome LIKE '%🌈%' OR bio LIKE '%🌈%' OR nome LIKE '%⚧%' OR bio LIKE '%⚧%' OR bio LIKE '%ele%' OR bio LIKE '%ela%' OR bio LIKE '%elu%' OR bio LIKE '%pronome%'OR bio LIKE '%UFPR%' OR bio LIKE '%trans%' OR bio LIKE '%travesti%' OR bio LIKE '%trava%');"
	cursor.execute(sql)

	resultado = cursor.fetchall()
	for user in resultado:
		users.append(User(id=user[0],nome=user[1],bio=user[2],username=user[3],eu_sigo=user[4],cont_seguidores=user[5],cont_seguidos=user[6],protegido=user[7]))
	cursor.close()
	return users

def baixa_pesquisades(db_connection):
	cursor = db_connection.cursor()
	ids = []
	sql = "SELECT user_id FROM pesquisades"
	cursor.execute(sql)
	resultado = cursor.fetchall()

	for linha in resultado:
		ids.append(linha[0])
	cursor.close()
	resultado.clear()
	return ids

def inicia_pesquisa_bd(user, db_connection):
	cursor = db_connection.cursor()

	sql = "INSERT INTO pesquisades (user_id, data_inicio, hora_inicio) VALUES (%s, CURRENT_DATE, CURRENT_TIME)"
	cursor.execute(sql, (user.id,))

	cursor.close()
def conclui_pesquisa_bd(user, db_connection):
	cursor = db_connection.cursor()

	sql = ("UPDATE pesquisades set data_fim = CURRENT_DATE, hora_fim = CURRENT_TIME where user_id=%s")
	cursor.execute(sql, (user.id,))

	cursor.close()

def adiciona_user_bd(users, db_connection):
	cursor = db_connection.cursor()
	for user in users:
		sql = "INSERT IGNORE INTO users (id, nome, username, bio, me_segue, eu_sigo, cont_seguidores, cont_seguidos, foto, fechado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		#TODO: pq os seguidores e seguidos tão invertidos??
		values = (user.id, user.nome, user.username, user.bio, user.me_segue, user.eu_sigo, user.cont_seguidores, user.cont_seguidos, user.foto, user.protegido)
		cursor.execute(sql, values)

		if(cursor.rowcount == 0):
			atualiza_users_bd([user], db_connection)
		else:
			print("o registro de < " + user.nome + " > foi inserido.")
	cursor.close()

# TODO absurdo: me segue/eu sigo são opostos dicotomicos!!
# TODO: essa funçao só pega um por vez mesmo? pra que o for?
# TODO: pq ele atualiza TODA VEZ?
def atualiza_users_bd(users, db_connection):
	cursor = db_connection.cursor()
	for user in users:
		# Se a bio for apagada, não atualiza ela.
		if(user.bio != ""):
			sql = ("update users set bio = %s, nome = %s, username = %s, me_segue = %s, eu_sigo = %s, cont_seguidores = %s, cont_seguidos = %s, foto = %s, fechado = %s where id=%s")
			values = (user.bio, user.nome, user.username, user.me_segue, user.eu_sigo, user.cont_seguidores, user.cont_seguidos, user.foto, user.protegido, user.id)
		else:
			sql = ("update users set nome = %s, username = %s, me_segue = %s, eu_sigo = %s, cont_seguidores = %s, cont_seguidos = %s, foto = %s where id=%s")
			values = (user.nome, user.username, user.me_segue, user.eu_sigo, user.cont_seguidores, user.cont_seguidos, user.foto, user.id)
		cursor.execute(sql, values)
		print("as infos de < "+ user.nome +" > foram atualizadas.")
	# if cursor.rowcount != 0:
	# 	print(str(cursor.rowcount) + " registros foram atualizados.")

	cursor.close()