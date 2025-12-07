import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redireciona para login se não autenticado


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', '12345')


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)
    tipo = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    imagem_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Produto('{self.nome}', '{self.preco}')"


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USER and password == ADMIN_PASS:
            user = User(id=1)
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('login.html')


@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            descricao = request.form['descricao']
            preco = float(request.form['preco'])
            estoque = int(request.form['estoque'])
            tipo = request.form['tipo']
            categoria = request.form['categoria']
            imagem_url = request.form['imagem_url']

            if preco <= 0:
                flash('Preço deve ser maior que zero!', 'error')
                return redirect(url_for('admin'))

            if estoque < 0:
                flash('Estoque não pode ser negativo!', 'error')
                return redirect(url_for('admin'))

            novo_produto = Produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque=estoque,
                tipo=tipo,
                categoria=categoria,
                imagem_url=imagem_url
            )

            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('admin'))

        except ValueError:
            flash('Erro: Preço e Estoque devem ser números válidos.', 'error')
            return redirect(url_for('admin'))

        except KeyError as e:
            flash(f'Erro: Campo obrigatório faltando: {e}', 'error')
            return redirect(url_for('admin'))

    produtos = Produto.query.all()
    return render_template('admin.html', produtos=produtos)


@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)


@app.route('/biosseguranca')
def biosseguranca():
    return render_template('biosseguranca-page.html')


@app.route('/auricular')
def auricular():
    return render_template('auricular-page.html')


@app.route('/facial')
def facial():
    return render_template('facial-page.html')


@app.route('/gold')
def gold():
    produtos = Produto.query.filter_by(categoria='ouro').all()
    return render_template('gold-page.html', produtos=produtos)


@app.route('/prata')
def prata():
    produtos = Produto.query.filter_by(categoria='titanio').all()
    return render_template('prata-page.html', produtos=produtos)


@app.route('/zirconia')
def zirconia():
    produtos = Produto.query.filter_by(categoria='zirconia').all()
    return render_template('zirconia-page.html', produtos=produtos)


@app.route('/admin/produto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)

    if request.method == 'POST':
        try:
            produto.nome = request.form['nome'].strip()
            produto.descricao = request.form['descricao'].strip()
            produto.preco = float(request.form['preco'])
            produto.estoque = int(request.form['estoque'])
            produto.tipo = request.form['tipo'].strip()
            produto.imagem_url = request.form['imagem_url'].strip()

            if produto.preco <= 0:
                flash('❌ Preço deve ser maior que zero!', 'error')
                return redirect(url_for('editar_produto', id=id))

            if produto.estoque < 0:
                flash('Estoque não pode ser negativo!', 'error')
                return redirect(url_for('editar_produto', id=id))

            db.session.commit()
            flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'sucess')
            return redirect(url_for('admin'))

        except ValueError:
            flash('Erro: Preço e Estoque devem ser números válidos!', 'error')
        except Exception as e:
            flash(f'Erro ao atualizar: {str(e)}', 'error')

    return render_template('editar_produto.html', produto=produto)


@app.route('/admin/produto/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    nome_produto = produto.nome

    try:
        db.session.delete(produto)
        db.session.commit()
        flash ('Produto "{nome_produto}" excluído com sucesso!', 'success')
    except Exception as e:
        flash ('Erro ao excluir: {str(e)}', 'error')

    return redirect(url_for('admin'))

with app.app_context():
        db.create_all()
    #app.run(debug=os.getenv('DEBUG', 'False') == 'True')#

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', 'False') == 'True')