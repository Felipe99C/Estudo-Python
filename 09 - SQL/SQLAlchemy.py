"""
# Guia Resumido do SQLAlchemy: Conceitos Fundamentais

SQLAlchemy é uma biblioteca ORM (Object Relational Mapper) para Python que facilita a interação entre
o código Python e bancos de dados relacionais. Este guia explora seus conceitos principais.
"""

#------------------------------------------------------
# 1. Engine (Motor)
#------------------------------------------------------
"""
O Engine é o ponto de entrada para o SQLAlchemy. É o componente responsável pela comunicação 
entre seu código Python e o banco de dados. Ele gerencia conexões e traduz operações Python 
para comandos SQL.
"""

from sqlalchemy import create_engine

# Criação do engine com diferentes dialetos de banco de dados
# PostgreSQL
engine_pg = create_engine('postgresql://usuário:senha@localhost:5432/banco_de_dados', echo=True)

# MySQL
engine_mysql = create_engine('mysql+pymysql://usuário:senha@localhost/banco_de_dados', echo=True)

# SQLite (banco de dados em arquivo)
engine_sqlite = create_engine('sqlite:///banco_local.db', echo=True)

# O parâmetro echo=True habilita logs SQL para depuração


#------------------------------------------------------
# 2. Declarative Base (Base Declarativa)
#------------------------------------------------------
"""
A Base Declarativa é a classe fundamental da qual todos os modelos de tabelas herdam.
Ela contém a configuração e metadados necessários para mapear classes Python para tabelas SQL.
"""

from sqlalchemy.orm import declarative_base
# Antigamente era chamado de sqlalchemy.ext.declarative, em versões mais novas é sqlalchemy.orm

Base = declarative_base()


#------------------------------------------------------
# 3. Models (Modelos)
#------------------------------------------------------
"""
Os modelos são classes Python que representam tabelas no banco de dados. Cada atributo
da classe corresponde a uma coluna na tabela. Os relacionamentos entre tabelas são definidos
através desses modelos.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime

# Exemplo de modelo simples
class Usuario(Base):
    __tablename__ = 'usuarios'  # Nome da tabela no banco de dados
    
    # Colunas da tabela
    id = Column(Integer, primary_key=True)  # Chave primária
    nome = Column(String(100), nullable=False)  # String com tamanho máximo e não nula
    email = Column(String(100), unique=True)  # Valor único
    idade = Column(Integer)
    ativo = Column(Boolean, default=True)  # Valor padrão
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)  # Data automática
    
    # Representação para debugging
    def __repr__(self):
        return f"<Usuario(nome='{self.nome}', email='{self.email}')>"


# Exemplo de modelo com relacionamento
class Endereco(Base):
    __tablename__ = 'enderecos'
    
    id = Column(Integer, primary_key=True)
    rua = Column(String(100))
    cidade = Column(String(50))
    estado = Column(String(2))
    
    # Chave estrangeira que referencia a tabela de usuários
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    
    # Relacionamento com o modelo Usuario (permite acesso fácil entre objetos relacionados)
    usuario = relationship("Usuario", back_populates="enderecos")

# Adicionando o relacionamento reverso ao modelo Usuario
Usuario.enderecos = relationship("Endereco", back_populates="usuario")

# Criar todas as tabelas definidas no banco de dados
Base.metadata.create_all(engine_pg)


#------------------------------------------------------
# 4. Session (Sessão)
#------------------------------------------------------
"""
A Session é usada para gerenciar todas as operações no banco de dados. Ela estabelece e 
mantém as conversações com o banco e funciona como um buffer onde todas as operações 
são realizadas antes de serem efetivamente enviadas ao banco através de um commit.
"""

from sqlalchemy.orm import sessionmaker

# Criando uma fábrica de sessões
Session = sessionmaker(bind=engine_pg)

# Método tradicional (sem with)
session = Session()

try:
    # Criando e adicionando um novo usuário
    novo_usuario = Usuario(nome='Maria Silva', email='maria@exemplo.com', idade=30)
    session.add(novo_usuario)  # Adiciona à sessão (ainda não está no banco)
    
    # Adicionando múltiplos objetos
    session.add_all([
        Usuario(nome='João Santos', email='joao@exemplo.com', idade=25),
        Usuario(nome='Ana Oliveira', email='ana@exemplo.com', idade=28)
    ])
    
    # Confirma as operações (envia para o banco)
    session.commit()
except:
    # Em caso de erro, desfaz todas as operações
    session.rollback()
    raise
finally:
    # Sempre feche a sessão
    session.close()


###################### sempre tentar usar ###############################################
# Método moderno usando context manager (with)
with Session() as session:
    novo_endereco = Endereco(rua='Av. Brasil, 123', cidade='São Paulo', estado='SP', usuario_id=1)
    session.add(novo_endereco)
    # O commit é feito automaticamente ao sair do bloco if sem exceções
    # O rollback é chamado automaticamente se uma exceção ocorrer
    # A sessão é fechada automaticamente


#------------------------------------------------------
# 5. Queries (Consultas)
#------------------------------------------------------
"""
As consultas permitem buscar, filtrar e manipular dados no banco de dados. O SQLAlchemy
oferece uma API Python para construir consultas SQL de forma programática e segura.
"""

# Criando uma sessão para consultas
session = Session()

try:
    # Busca todos os usuários (SELECT * FROM usuarios)
    todos_usuarios = session.query(Usuario).all()
    
    # Busca o primeiro usuário com nome 'Maria Silva'
    maria = session.query(Usuario).filter_by(nome='Maria Silva').first()
    
    # Busca usando filtros mais complexos
    usuarios_ativos = session.query(Usuario).filter(
        Usuario.ativo == True,
        Usuario.idade > 25
    ).order_by(Usuario.nome).all()
    
    # Contagem de registros
    total_usuarios = session.query(Usuario).count()
    
    # Consultando com joins (usuários e seus endereços)
    resultados = session.query(Usuario, Endereco).join(Endereco).all()
    for usuario, endereco in resultados:
        print(f"{usuario.nome} mora em {endereco.cidade}-{endereco.estado}")
    
    # Atualizando registros
    usuario_para_atualizar = session.query(Usuario).filter_by(email='maria@exemplo.com').first()
    if usuario_para_atualizar:
        usuario_para_atualizar.idade = 31
        session.commit()
    
    # Excluindo registros
    usuario_para_excluir = session.query(Usuario).filter_by(email='joao@exemplo.com').first()
    if usuario_para_excluir:
        session.delete(usuario_para_excluir)
        session.commit()
        
finally:
    session.close()


#------------------------------------------------------
# 6. Migrations (Migrações) com Alembic
#------------------------------------------------------
"""
O Alembic é uma ferramenta de migração para SQLAlchemy que permite evoluir seu esquema de banco
de dados de forma controlada. Ele registra cada alteração no esquema e permite aplicar ou
reverter essas alterações de forma sequencial.
"""

# Instalação: pip install alembic
# Inicialização: alembic init migrations
# Criar uma migração: alembic revision -m "criar tabela usuarios"
# Aplicar migrações: alembic upgrade head
# Voltar uma versão: alembic downgrade -1

# Exemplo básico de um script de migração Alembic
"""
# migrations/versions/1234567890_criar_tabela_usuarios.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), unique=True),
        sa.Column('idade', sa.Integer()),
    )

def downgrade():
    op.drop_table('usuarios')
"""


#------------------------------------------------------
# 7. Core vs ORM
#------------------------------------------------------
"""
O SQLAlchemy tem duas abordagens principais:
- Core: API mais próxima do SQL, com controle detalhado sobre as consultas
- ORM: Trabalha com classes e objetos Python (o que vimos até agora)

A abordagem Core é útil quando você precisa de máximo desempenho ou quando precisa
executar consultas SQL mais complexas e específicas.
"""

# Exemplo usando SQLAlchemy Core
from sqlalchemy import Table, MetaData, select

metadata = MetaData()

# Definição de tabela usando Core
usuarios_table = Table(
    'usuarios',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(100)),
    Column('email', String(100))
)

# Executando operações com Core
with engine_pg.connect() as conn:
    # Inserção
    conn.execute(usuarios_table.insert().values(
        nome='Roberto Core', 
        email='roberto@exemplo.com'
    ))
    
    # Consulta
    result = conn.execute(select([usuarios_table]))
    for row in result:
        print(row)


#------------------------------------------------------
# 8. Boas Práticas e Dicas
#------------------------------------------------------
"""
- Use sessões com with sempre que possível para garantir que conexões sejam fechadas
- Aproveite os tipos específicos de cada banco de dados para melhor desempenho
- Use lazy='joined' ou eager loading para evitar o problema N+1 de consultas
- Configure índices para campos frequentemente consultados
- Use profiling para identificar consultas lentas e otimizá-las
"""

# Exemplo de configuração avançada de Engine
engine_otimizado = create_engine(
    'postgresql://usuário:senha@localhost/banco',
    pool_size=10,  # Tamanho do pool de conexões
    max_overflow=20,  # Máximo de conexões extras
    pool_timeout=30,  # Timeout em segundos
    pool_recycle=1800,  # Recicla conexões após 30 minutos
    echo=False  # Desativa logs em produção
)

# Exemplo de lazy loading vs eager loading
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200))
    autor_id = Column(Integer, ForeignKey('usuarios.id'))
    
    # Lazy loading (padrão) - carrega comentários apenas quando acessados
    comentarios = relationship("Comentario", lazy='select')
    
    # Eager loading - carrega comentários junto com o post
    # comentarios = relationship("Comentario", lazy='joined')

class Comentario(Base):
    __tablename__ = 'comentarios'
    
    id = Column(Integer, primary_key=True)
    texto = Column(String(500))
    post_id = Column(Integer, ForeignKey('posts.id'))


#------------------------------------------------------
# 9. Performance e Tunning
#------------------------------------------------------
"""
A performance em SQLAlchemy pode ser otimizada usando:
- Consultas específicas vs consultas genéricas
- Escolhendo estratégias de lazy loading adequadas
- Usando bulk operations para grandes conjuntos de dados
- Utilizando consultas compiladas para operações repetitivas
"""

# Exemplo de bulk insert (muito mais rápido para múltiplos registros)
session = Session()
try:
    # Ao invés de:
    # for i in range(1000):
    #     user = Usuario(nome=f"Usuário {i}", email=f"usuario{i}@exemplo.com")
    #     session.add(user)
    
    # Use bulk_insert_mappings:
    usuarios_dados = [
        {"nome": f"Usuário {i}", "email": f"usuario{i}@exemplo.com"} 
        for i in range(1000)
    ]
    session.bulk_insert_mappings(Usuario, usuarios_dados)
    session.commit()
finally:
    session.close()


#------------------------------------------------------
# 10. SQLAlchemy 2.0 (Novidades)
#------------------------------------------------------
"""
A versão 2.0 introduziu várias mudanças importantes:
- Nova API de consulta (select() em vez de query())
- Melhor suporte a tipagem para integração com sistemas de tipo Python
- Remoção de APIs legadas marcadas como deprecated
- Melhor integração com recursos assíncronos
"""

# SQLAlchemy 2.0 - Nova API de consulta
from sqlalchemy import select

with Session() as session:
    # Consulta tradicional (1.x)
    usuario_1x = session.query(Usuario).filter_by(id=1).first()
    
    # Nova consulta (2.0)
    stmt = select(Usuario).where(Usuario.id == 1)
    usuario_2x = session.execute(stmt).scalars().first()