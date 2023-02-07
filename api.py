from flask import Flask, jsonify, request
import sqlite3

#Configurações inicias
app = Flask(__name__)

#Rotas iniciais
#lista todos
@app.route('/produtos', methods=['GET'])
def listaTodosOsProdutos():
	#Fazendo a consulta no banco de dados
	banco = sqlite3.connect('estoque.db')
	cursor = banco.cursor()
	cursor.execute("SELECT * FROM produtos")
	informacoes_do_banco = cursor.fetchall()
	banco.commit()
	banco.close()

	#Retornando os produtos cadastradas no banco
	return jsonify(informacoes_do_banco)

#Busca um produto pelo nome
@app.route('/produtos/<string:nome>', methods=['GET'])
def retornaProdutoPeloNome(nome):
	banco = sqlite3.connect('estoque.db')
	cursor = banco.cursor()
	cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
	resultado = cursor.fetchone()
	banco.commit()
	banco.close()

	if resultado == None:
		return jsonify({"mensagem": 'Produto não encontrado'})
	else:
		return jsonify(resultado)

#Alterando um produto
@app.route('/produtos/alterar/<string:nome>', methods=['PUT'])
def alterandoProduto (nome):
	banco = sqlite3.connect('estoque.db')
	cursor = banco.cursor()
	cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
	resultado = cursor.fetchone()
	if resultado:
		nome_do_produto = request.json['nome']
		nova_quantidade = request.json['quantidade_no_estoque']
		novo_valor = request.json['valor_pago']
		cursor.execute("UPDATE produtos SET nome = ?, quantidade_no_estoque = ?, valor_pago = ? WHERE nome = ?", (nome_do_produto, nova_quantidade,novo_valor, nome))
		banco.commit()
		banco.close()
		return jsonify({"mensagem": "Produto atualizado com sucesso!"})
	else:
		banco.close()
		return jsonify({"mensagem": "Produto não encontrado"})
		
#Criando Produto no banco de dados
@app.route('/produtos/cadastrar', methods=['POST'])
def cadastrandoProdutosNoBancoDeDados ():
	novo_produto_nome = request.json['nome'].strip()
	novo_produto_quantidade = request.json['quantidade_no_estoque']
	novo_produto_valor = request.json['valor_pago']
	banco = sqlite3.connect('estoque.db')
	cursor = banco.cursor()
	cursor.execute("SELECT * FROM produtos WHERE nome = ?", (novo_produto_nome,))
	resultado = cursor.fetchone()
	if resultado:
		banco.close()
		return jsonify({"mensagem": "Produto já cadastrado!"})	
	else: 
		cursor.execute("INSERT INTO produtos (nome, quantidade_no_estoque, valor_pago) VALUES (?, ?, ?)", (novo_produto_nome, novo_produto_quantidade, novo_produto_valor))
		banco.commit()
		banco.close()
		return jsonify({"mensagem": "Produto cadastrado com sucesso!"})

#Excluindo produtos do banco de dados
@app.route('/produtos/excluir/<string:nome>', methods=['DELETE'])
def excluindoProdutosDoBancoDeDados (nome):
	banco = sqlite3.connect('estoque.db')
	cursor = banco.cursor()
	cursor.execute('SELECT * FROM produtos WHERE nome=?', (nome,))
	produto = cursor.fetchone()
	if produto == None:
		banco.close()
		return jsonify({"mensagem": 'Produto não encontrado!'})
	else:
		cursor.execute('DELETE FROM produtos WHERE nome=?', (nome,))
		banco.commit()
		banco.close()
		return jsonify({"mensagem": 'Produto excluido com sucesso!'})


#Fornecendo porta para rodar a api
app.run(port=8080, host='localhost', debug=True)
