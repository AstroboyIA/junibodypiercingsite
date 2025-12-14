import os
import mercadopago
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///test.db'
)
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
ADMIN_PASS = os.getenv('ADMIN_PASS', 'astroboypassword')

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    pedidos = db.Relationship('Pedido', backref='comprador', lazy=True)

    def __repr__(self):
        return f"Usuario('{self.nome}', '{self.email}')"


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

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='Pendente')
    total = db.Column(db.Float, nullable=False)

    itens = db.Relationship('ItemPedido', backref='pedido', lazy=True)

    def __repr__(self):
        return f"Pedido('{self.id}', '{self.data_pedido}', '{self.status}')"

class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    produto = db.Relationship('Produto')

    def __repr__(self):
        return f"ItemPedido('{self.pedido_id}', '{self.produto_id}', '{self.quantidade}')"

@app.route('/checkout', methods=['GET', 'POST'])
login_required
def checkout():
    usuario_id_logado = current_user.id

    if request.method == 'GET':
        itens_carrinho = []
        subtotal = 0

        if 'carrinho' in session and session['carrinho']:

            if not intans_carrinho:
                return redirect(url_for('visualizar_carrinho'))

        return render_template('checkout.html', itens_carrinho=intens_carrinho, subtotal=subtotal)


                   '''!!!!!!!!!!!!!!!!!!!!! PAREI AQUI !!!!!!!!!!!!!!!!!!!'''
                   '''!!!!!!!!!!!!!!!!!!!!! PAREI AQUI !!!!!!!!!!!!!!!!!!!'''
                   '''!!!!!!!!!!!!!!!!!!!!! PAREI AQUI !!!!!!!!!!!!!!!!!!!'''

@app.route('/carrinho/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    if 'carrinho' not in session:
        session['carrinho'] = {}

        quantidade = int(request.form.get('quantidade', 1))
        carrinho = session['carrinho']

        if str(produto_id) in carrinho:
            carrinho[str(produto_id)] += quantidade
        else:
            carrinho[str(produto_id)] = quantidade

        session.modified = True

        return redirect(url_for('index'))

@app.route('/carrinho')
def visualizar_carrinho():
    carrinho_data = []
    subtotal = 0

    if 'carrinho' in session and session['carrinho']:
        ids_produtos = list(sessio['carrinho'].keys())
        
        ids_int = [int(p_id) for p_id in ids_produtos]

        produtos = Produto.query.filter(Protudo.id.in_(ids_int)).all()

        for produto in produtos:
            quantidade = session ['carrinho'][str(produto.id)]
            total_item = produto.preco * quantidade
            subtotal += total_item

            carrinho_data.append({
                'produto': produto,
                'quantidade': quantidade,
                'total_item': total_item
            })

    return render_template('carrinho.html', carrinho=carrinho_data, subtotal=subtotal)

@app.route('/carrinho/remover/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    str_id = str(produto_id)
    if 'carrinho' in session and str_id in session['carrinho']:
        carrinho = session['carrinho']

        del carrinho[str_id]

        session.modified = True

        flash('Produto removido do carrinho com sucesso!', 'success')

    return redirect(url_for('visualizar_carrinho'))

@app.route('/carrinho/atualizar', methods=['POST'])
def atualizar_carrinho():
    if 'carrinho ' not in session:
        return redirect(url_for('visualizar_carrinho'))

        carrinho = session['carrinho']

        for key, Value in request.form.items():
            try:
                produto_id = int(key)
                nova_quantidade = int(value)
                str_id = str(produto_id)

                if str_id in carrinho:
                    if nova_quantidade > 0:
                        carrinho[str_id] = nova_quantidade
                    else:
                        del carrinho[str_id]

            except ValueError:
                pass

        session.modified = True

        return redirect(url_for('visualizar_carrinho'))


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
            produto.categoria = request.form['categoria']
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