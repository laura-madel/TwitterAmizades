# Baixa do BD todes ês usuáries que já foram pesquisades ou que tem perfil fechado (erro_na_pesquisa) para não serem pesquisades novamente.
def baixa_pesquisades(conexao_bd):
	cursor = conexao_bd.cursor()
	ids = []
	sql = "SELECT id_usuarie FROM pesquisas WHERE fim IS NOT NULL OR erro_na_pesquisa is TRUE"
	cursor.execute(sql)
	resultado = cursor.fetchall()

	for linha in resultado:
		ids.append(linha[0])
	cursor.close()
	resultado.clear()
	return ids

# Registra a data e horário de início da pesquisa, usa o id dê usuárie
def inicia_pesquisa_bd(usuarie, conexao_bd):
	cursor = conexao_bd.cursor()

	sql = "INSERT INTO pesquisas (id_usuarie, inicio) VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE inicio=NOW()"
	cursor.execute(sql, (usuarie.id,))

	cursor.close()

def registra_erro_pesquisa_bd(usuarie, conexao_bd):
	cursor = conexao_bd.cursor()

	sql = ("UPDATE pesquisas set erro_na_pesquisa = TRUE where id_usuarie=%s")
	cursor.execute(sql, (usuarie.id,))

	cursor.close()

def conclui_pesquisa_bd(usuarie, conexao_bd):
	cursor = conexao_bd.cursor()

	sql = ("UPDATE pesquisas set fim = NOW() where id_usuarie=%s")
	cursor.execute(sql, (usuarie.id,))

	cursor.close()
