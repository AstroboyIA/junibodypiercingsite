from app import db, Produto, app

app.app_context().push()


db.drop_all()
db.create_all()

print("Tabelas recriadas com sucesso.")

p1 = Produto(
    nome='Piercing Argola Ouro 18K',
    descricao='Joia maciça em ouro 18K.',
    preco=350.00,
    estoque=5,
    tipo='18K Gold',
    imagem_url='images/orelha-ouro.jpg'
)
p2 = Produto(
    nome='Labret Titânio Zircônia',
    descricao='Titânio ASTM F-136, hipoalergênico.',
    preco=120.00,
    estoque=12,
    tipo='ASTM F-136',
    imagem_url='images/orelha-prata.jpg'
)

db.session.add_all([p1, p2])
db.session.commit()

print("Produtos inseridos com sucesso!")
print(Produto.query.all())