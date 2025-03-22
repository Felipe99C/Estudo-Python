# Desafio Intermediário usando SQLModel: Tabelas de Produto e Fornecedor
'''
-> Este desafio focará na criação de duas tabelas relacionadas, Produto e Fornecedor, utilizando SQLModel.
-> Cada produto terá um fornecedor associado, demonstrando o uso de relacionamentos para estabelecer conexões entre tabelas.
-> Além disso, você realizará inserções nessas tabelas para praticar a manipulação de dados.
'''

#%%
# Importando as bibliotecas necessárias
from sqlmodel import Field, SQLModel, Session, create_engine, select, Relationship
from typing import Optional, List
from sqlalchemy import func

# Criando os modelos (SQLModel substitui a Base e as classes que herdam dela)
class Fornecedor(SQLModel, table=True):
    __tablename__ = 'fornecedores'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    
    # Relacionamento reverso - não é armazenado no BD, apenas para acesso em Python
    produtos: List["Produto"] = Relationship(back_populates="fornecedor")


class Produto(SQLModel, table=True):
    __tablename__ = 'produtos'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: Optional[str] = None
    preco: Optional[int] = None
    
    # Campo de chave estrangeira
    fornecedor_id: Optional[int] = Field(default=None, foreign_key="fornecedores.id")
    
    # Relacionamento com Fornecedor
    fornecedor: Optional[Fornecedor] = Relationship(back_populates="produtos")

# Resolvendo referências circulares
SQLModel.update_forward_refs()

#%%
# Cria o Banco de Dados e as Tabelas

# Criando a engine de conexão com o banco de dados
engine = create_engine('sqlite:///desafio.db', echo=True)

# Criando todas as tabelas
SQLModel.metadata.create_all(engine)

# Criando uma sessão
with Session(engine) as session:
    # Inserindo fornecedores
    fornecedores = [
        Fornecedor(nome="Fornecedor A", telefone="123456789", email="contato@a.com", endereco="Endereço A"),
        Fornecedor(nome="Fornecedor B", telefone="123456789", email="contato@b.com", endereco="Endereço B"),
        Fornecedor(nome="Fornecedor C", telefone="123456789", email="contato@c.com", endereco="Endereço C"),
        Fornecedor(nome="Fornecedor D", telefone="123456789", email="contato@d.com", endereco="Endereço D"),
        Fornecedor(nome="Fornecedor E", telefone="123456789", email="contato@e.com", endereco="Endereço E")
    ]
    
    session.add_all(fornecedores)
    session.commit()
    
    # Buscando os IDs gerados para usar nos produtos
    for fornecedor in fornecedores:
        print(f"Fornecedor {fornecedor.nome} tem ID {fornecedor.id}")
    
    # Inserindo produtos
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
with Session(engine) as session:
    # Consulta usando o select do SQLModel (estilo SQLAlchemy 2.0)
    statement = select(Produto)
    produtos = session.exec(statement).all()
    
    # Exibindo os produtos e seus fornecedores
    for produto in produtos:
        print(f"Produto: {produto.nome} - Fornecedor: {produto.fornecedor.nome}")

#%%
# Mesma query em SQL só que usando SQLModel
'''
SELECT fornecedores.nome, SUM(produtos.preco) AS total_preco
FROM produtos
JOIN fornecedores ON produtos.fornecedor_id = fornecedores.id
GROUP BY fornecedores.nome;
'''

with Session(engine) as session:
    # No SQLModel, usamos a API do SQLAlchemy 2.0
    from sqlalchemy import select as sa_select
    
    # Criando a consulta com funções de agregação
    statement = sa_select(
        Fornecedor.nome,
        func.sum(Produto.preco).label('total_preco')
    ).join(
        Produto, Fornecedor.id == Produto.fornecedor_id
    ).group_by(
        Fornecedor.nome
    )
    
    # Executando a consulta
    resultado = session.exec(statement).all()
    
    # Exibindo os resultados
    for nome, total_preco in resultado:
        print(f"Fornecedor: {nome} - Total de Preço: {total_preco}")

#%%
# Exemplo adicional: Consulta usando relacionamentos do SQLModel
with Session(engine) as session:
    # Buscar todos os fornecedores com seus produtos
    statement = select(Fornecedor)
    fornecedores = session.exec(statement).all()
    
    for fornecedor in fornecedores:
        print(f"Fornecedor: {fornecedor.nome}")
        print(f"  Produtos ({len(fornecedor.produtos)}):")
        for produto in fornecedor.produtos:
            print(f"    - {produto.nome}: R${produto.preco}")
        print("-" * 40)

#%%
# Exemplo de atualização de dados
with Session(engine) as session:
    # Buscar um produto específico
    statement = select(Produto).where(Produto.nome == "Produto 1")
    produto = session.exec(statement).one()
    
    # Atualizar o preço
    print(f"Preço atual do {produto.nome}: {produto.preco}")
    produto.preco = 150
    session.add(produto)
    session.commit()
    
    # Verificar a atualização
    produto_atualizado = session.exec(
        select(Produto).where(Produto.id == produto.id)
    ).one()
    print(f"Novo preço do {produto_atualizado.nome}: {produto_atualizado.preco}")