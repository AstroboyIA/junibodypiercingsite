# insert_data.py

from app import db, Produto, app

# 1. Coloca a aplicação em contexto
app.app_context().push()

# 2. **ATENÇÃO:** Garante que o DB seja recriado (apague o test.db antes de rodar este script)
db.drop_all()  # Opção de segurança para dropar as tabelas antigas
db.create_all()

print("Tabelas recriadas com sucesso.")

# 3. CRIA OS OBJETOS DE PRODUTO COM A BARRA CORRETA
p1 = Produto(
    nome='Piercing Argola Ouro 18K',
    descricao='Joia maciça em ouro 18K.',
    preco=350.00,
    estoque=5,
    tipo='18K Gold',
    imagem_url='images/orelha-ouro.jpg'  # <-- Caminho correto
)
p2 = Produto(
    nome='Labret Titânio Zircônia',
    descricao='Titânio ASTM F-136, hipoalergênico.',
    preco=120.00,
    estoque=12,
    tipo='ASTM F-136',
    imagem_url='images/orelha-prata.jpg' # <-- Caminho correto
)

# 4. Adiciona e Salva no banco de dados
db.session.add_all([p1, p2])
db.session.commit()

# 5. Confirmação
print("Produtos inseridos com sucesso!")
print(Produto.query.all())