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

def adiciona_user_bd(db_connection, id, nome, username, bio =""):
	cursor = db_connection.cursor()

	sql = "INSERT IGNORE INTO users (id, nome, username, bio) VALUES (%s, %s, %s, %s)"
	values = (id, nome, username, bio)
	cursor.execute(sql, values)

	if(cursor.rowcount == 0):
		atualiza_user_bd(db_connection, id, nome, username, bio)
	else:
		print("o registro de " + nome + " foi inserido.")
	cursor.close()

def atualiza_user_bd(db_connection, id, nome, username, bio=""):
	cursor = db_connection.cursor()

	if(bio != ""):
		sql = ("update users set bio = %s, nome = %s, username = %s where id=%s")
		values = (bio, nome, username, id)
	else:
		sql = ("update users set nome = %s, username = %s where id=%s")
		values = (nome, username, id)

	cursor.execute(sql, values)
	if cursor.rowcount != 0:
		print("o registro de " + nome + " foi atualizado.")

	cursor.close()

def adiciona_bio_bd(db_connection, id, bio):

	cursor = db_connection.cursor()
	sql = ("update users set bio = %s where id=%s")
	values = (bio, id)
	cursor.execute(sql, values)
	if cursor.rowcount != 0:
		print("nova bio inserida: " + bio)

	cursor.close()