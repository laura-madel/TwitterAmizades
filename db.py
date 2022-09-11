import mysql.connector
from mysql.connector import errorcode

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

def adiciona_user_bd(users, db_connection):
	cursor = db_connection.cursor()
	for user in users:
		sql = "INSERT IGNORE INTO users (id, nome, username, bio) VALUES (%s, %s, %s, %s)"
		values = (user.id, user.nome, user.username, user.bio)
		cursor.execute(sql, values)

		if(cursor.rowcount == 0):
			atualiza_users_bd([user], db_connection)
		else:
			print("o registro de " + user.nome + " foi inserido.")
	cursor.close()

def atualiza_users_bd(users, db_connection):
	cursor = db_connection.cursor()
	for user in users:
		if(user.bio != ""):
			sql = ("update users set bio = %s, nome = %s, username = %s where id=%s")
			values = (user.bio, user.nome, user.username, user.id)
		else:
			sql = ("update users set nome = %s, username = %s where id=%s")
			values = (user.nome, user.username, user.id)
		cursor.execute(sql, values)
	if cursor.rowcount != 0:
		print(str(cursor.rowcount) + " registros foram atualizados.")

	cursor.close()