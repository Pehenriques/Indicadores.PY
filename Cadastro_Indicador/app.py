from flask import Flask, render_template, request, jsonify
import mysql.connector
import webbrowser
import threading
from datetime import datetime

app = Flask(__name__)

# Conexão com MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="indicadores_db"
    )

def abrir_navegador():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/indicadores')
def indicadores():
    return render_template('indicadores.html')

@app.route('/editar_indicador')
def editar_indicador():
    id = request.args.get("id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM indicadores WHERE id = %s", (id,))
    indicador = cursor.fetchone()

    cursor.close()
    conn.close()

    if not indicador:
        return "Indicador não encontrado", 404

    return render_template("editar_indicador.html", indicador=indicador)


@app.route('/atualizar_indicador', methods=['POST'])
def atualizar_indicador():
    id = request.form["id"]
    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    cpf = request.form["cpf"]
    endereco = request.form["endereco"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE indicadores SET nome=%s, email=%s, telefone=%s, cpf=%s, endereco=%s WHERE id=%s
    """, (nome, email, telefone, cpf, endereco, id))

    conn.commit()
    cursor.close()
    conn.close()

    # Recarrega os dados do indicador atualizado
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM indicadores WHERE id = %s", (id,))
    indicador = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('editar_indicador.html', indicador=indicador, mensagem="Indicador atualizado com sucesso!")

@app.route('/cadastro_prestador')
def cadastro_prestador():
    indicador_id = request.args.get("indicador")
    return render_template('cadastro_prestador.html', indicador_id=indicador_id)

@app.route('/salvar_dados', methods=['POST'])
def salvar_dados():
    dados = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO indicadores 
        (nome, email, telefone, cpf, endereco, codigo_indicador, link_indicador, data_cadastro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    codigo = f"{int(datetime.now().timestamp())}{dados['cpf'][-4:]}"
    link = f"http://127.0.0.1:5000/cadastro_prestador?indicador={codigo}"
    
    cursor.execute(sql, (
        dados["nome"], dados["email"], dados["telefone"], dados["cpf"],
        dados["endereco"], codigo, link, datetime.now()
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Indicador cadastrado com sucesso!", "link": link}), 201

@app.route('/salvar_prestador', methods=['POST'])
def salvar_prestador():
    dados = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM indicadores WHERE codigo_indicador = %s", (dados["indicador_id"],))
    resultado = cursor.fetchone()
    if not resultado:
        return jsonify({"mensagem": "Indicador não encontrado."}), 404

    indicador_id = resultado[0]

    cursor.execute("""
        INSERT INTO prestadores (nome, email, telefone, cpf, cidade, estado, indicador_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        dados["nome"], dados["email"], dados["telefone"],
        dados["cpf"], dados["cidade"], dados["estado"], indicador_id
    ))

    prestador_id = cursor.lastrowid

    for maquina in dados["maquinas"]:
        cursor.execute("""
            INSERT INTO maquinas (prestador_id, tipo, modelo, ano, implemento, descricao)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            prestador_id, maquina["tipo"], maquina["modelo"],
            maquina["ano"], maquina.get("implemento"), maquina.get("descricao")
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Prestador e máquinas cadastrados com sucesso!"}), 201

@app.route('/listar_dados', methods=['GET'])
def listar_dados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM indicadores")
    indicadores = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(indicadores), 200

@app.route('/deletar_dados/<id>', methods=['DELETE'])
def deletar_dados(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM indicadores WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensagem": f"Indicador {id} deletado com sucesso."}), 200

if __name__ == '__main__':
    threading.Timer(1.5, abrir_navegador).start()
    app.run(debug=True)
