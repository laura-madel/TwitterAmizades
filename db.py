import mysql.connector
from mysql.connector import errorcode
from User import *

#!#! TODO: Descobrir como adicionar/atualizar mais de um registro por vez no MySQL.

def conectar_bd():
	try:
		db_connection = mysql.connector.connect(host='162.214.166.89', user='lauramadel', password='7he2ya984bcl', database='amizades')
		print("Conectado com o banco de dados!")
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
	sql = "SELECT id, nome, bio, username FROM users WHERE bio NOT LIKE '%🔞%' AND nome NOT LIKE '%🔞%' AND (nome LIKE '%🌈%' OR bio LIKE '%🌈%' OR nome LIKE '%⚧%' OR bio LIKE '%⚧%' OR bio LIKE '%ele%' OR bio LIKE '%ela%' OR bio LIKE '%elu%' OR bio LIKE '%pronome%'OR bio LIKE '%UFPR%' OR bio LIKE '%trans%' OR bio LIKE '%travesti%' OR bio LIKE '%trava%');"
	cursor.execute(sql)

	resultado = cursor.fetchall()
	for user in resultado:
		users.append(User(id=user[0],nome=user[1],bio=user[2],username=user[3]))
	cursor.close()
	return users

def adiciona_pesquisade(user, db_connection):
	cursor = db_connection.cursor()

	sql = "INSERT INTO pesquisades (id, data_pesquisa) VALUES (%s, CURRENT_DATE)"
	values = (user.id)
	cursor.execute(sql, values)

	cursor.close()

def verifica_se_ja_pesquisou(user, db_connection):
	cursor = db_connection.cursor()

	sql = "SELECT id, nome, bio, username FROM pesquisades WHERE id = %s;"
	values = (user.id)
	cursor.execute(sql, values)
	if cursor.rowcount > 0:
		cursor.close()
		return True
	cursor.close()
	return False
def adiciona_user_bd(users, db_connection):
	cursor = db_connection.cursor()
	for user in users:
		sql = "INSERT IGNORE INTO users (id, nome, username, bio, me_segue, eu_sigo, cont_seguidores, cont_seguidos, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (user.id, user.nome, user.username, user.bio, user.me_segue, user.eu_sigo, user.cont_seguidores, user.cont_seguidos, user.foto)
		cursor.execute(sql, values)

		if(cursor.rowcount == 0):
			atualiza_users_bd([user], db_connection)
		else:
			print("o registro de " + user.nome + " foi inserido.")
	cursor.close()

def atualiza_users_bd(users, db_connection):
	cursor = db_connection.cursor()
	for user in users:
		# Se a bio for apagada, não atualiza ela.
		if(user.bio != ""):
			sql = ("update users set bio = %s, nome = %s, username = %s, me_segue = %s, eu_sigo = %s, cont_seguidores = %s, cont_seguidos = %s, foto = %s where id=%s")
			values = (user.bio, user.nome, user.username, user.me_segue, user.eu_sigo, user.cont_seguidores, user.cont_seguidos, user.foto, user.id)
		else:
			sql = ("update users set nome = %s, username = %s, me_segue = %s, eu_sigo = %s, cont_seguidores = %s, cont_seguidos = %s, foto = %s where id=%s")
			values = (user.nome, user.username, user.me_segue, user.eu_sigo, user.cont_seguidores, user.cont_seguidos, user.foto, user.id)
		cursor.execute(sql, values)
	if cursor.rowcount != 0:
		print(str(cursor.rowcount) + " registros foram atualizados.")

	cursor.close()