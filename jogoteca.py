from flask import Flask, render_template, request, redirect, session, flash, url_for

from models.jogo import Jogo
from models.usuario import Usuario

primeiroJogo = Jogo('Tetris', 'Puzzle', 'Atari')
segundoJogo = Jogo('God of War', 'Rack n Slash', 'PS2')
terceiroJogo = Jogo('Skyrim', 'RPG', 'PC')
listaJogos = [primeiroJogo, segundoJogo, terceiroJogo]

usuario1 = Usuario('Kevin', 'KV', 'alohomora')
usuario2 = Usuario('Bruna', 'BS', 'xuxu')
usuario3 = Usuario('Guilherme', 'Gui', 'chocolate')

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}

app = Flask(__name__)
app.secret_key = 'alura'

app = Flask(__name__)
app.secret_key = 'alura'


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=listaJogos)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    listaJogos.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form_usuario = request.form['usuario']
    lista_usuarios = usuarios.values()
    for usuario in lista_usuarios:
        if usuario.nome == form_usuario and request.form['senha'] == usuario.senha:
            session['usuario_logado'] = form_usuario
            flash('Seja bem vindo(a), ' + form_usuario)
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    flash('Falha ao validar dados de login. Favor tente novamente')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


app.run(debug=True)
