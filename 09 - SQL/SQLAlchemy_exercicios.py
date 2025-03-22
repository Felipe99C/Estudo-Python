#%%
# Desafio Intermediário de SQLAlchemy: Tabelas de Produto e Fornecedor
'''
-> Este desafio focará na criação de duas tabelas relacionadas, Produto e Fornecedor, utilizando SQLAlchemy.
-> Cada produto terá um fornecedor associado, demonstrando o uso de chaves estrangeiras para estabelecer relações entre tabelas.
-> Além disso, você realizará inserções nessas tabelas para praticar a manipulação de dados.
'''

# Importando as bibliotecas necessárias	
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Criando a base abstrata
Base = declarative_base()

# Criando a classe Fornecedor
class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    telefone = Column(String(20))
    email = Column(String(50))
    endereco = Column(String(100))

# Criando a classe Produto
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(200))
    preco = Column(Integer)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
   
   # Estabelece a relação entre Produto e Fornecedor
    fornecedor = relationship("Fornecedor")
#%%
#Cria o Banco de Dados e as Tabelas

# Criando a engine de conexão com o banco de dados
#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///desafio.db', echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

Forncedores = [
Fornecedor(nome = "Fornecedor A", telefone = "123456789", email = "contato@a.com", endereco = "Endereço A"),
Fornecedor(nome = "Fornecedor B", telefone = "123456789", email = "contato@b.com", endereco = "Endereço B"),
Fornecedor(nome = "Fornecedor C", telefone = "123456789", email = "contato@c.com", endereco = "Endereço C"),
Fornecedor(nome = "Fornecedor D", telefone = "123456789", email = "contato@d.com", endereco = "Endereço D"),
Fornecedor(nome = "Fornecedor E", telefone = "123456789", email = "contato@e.com", endereco = "Endereço E")
]

session.add_all(Forncedores)
session.commit()

produtos = [
    Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=100, fornecedor_id=1),
    Produto(nome="Produto 2", descricao="Descrição do Produto 2", preco=200, fornecedor_id=2),
    Produto(nome="Produto 3", descricao="Descrição do Produto 3", preco=300, fornecedor_id=3),
    Produto(nome="Produto 4", descricao="Descrição do Produto 4", preco=400, fornecedor_id=4),
    Produto(nome="Produto 5", descricao="Descrição do Produto 5", preco=500, fornecedor_id=5)
]

session.add_all(produtos)
session.commit()

#%%
# Consultando os Dados
for produto in session.query(Produto).all():
    print(f"Produto: {produto.nome} - Fornecedor: {produto.fornecedor.nome}")

#%%
#mesma query em SQL só que usando alchemy
'''
SELECT fornecedores.nome, SUM(produtos.preco) AS total_preco
FROM produtos
JOIN fornecedores ON produtos.fornecedor_id = fornecedores.id
GROUP BY fornecedores.nome;
'''

Session = sessionmaker(bind=engine)
session = Session()

resultado = session.query(
    Fornecedor.nome,
    func.sum(Produto.preco).label('total_preco')
).join(Produto, Fornecedor.id == Produto.fornecedor_id
).group_by(Fornecedor.nome).all()

for nome,total_preco in resultado:
    print(f"Fornecedor: {nome} - Total de Preço: {total_preco}")
# %%
