"""
# Guia Resumido do SQLModel: Conceitos Fundamentais

SQLModel é uma biblioteca que une o melhor do SQLAlchemy (ORM para bancos de dados) e 
do Pydantic (validação de dados e serialização). Criada por Sebastián Ramírez 
(criador do FastAPI), o SQLModel simplifica a interação entre APIs e bancos de dados.
"""

#------------------------------------------------------
# 1. Instalação e Importações Básicas
#------------------------------------------------------
"""
O SQLModel é instalado via pip e importa funcionalidades tanto do SQLAlchemy
quanto do Pydantic de forma transparente para o usuário.
"""

# Instalação: pip install sqlmodel

# Importações básicas
from sqlmodel import SQLModel, Field, Session, select, create_engine
from typing import Optional, List
import datetime


#------------------------------------------------------
# 2. Definição de Modelos
#------------------------------------------------------
"""
No SQLModel, um único modelo serve para:
- Definir tabelas no banco de dados
- Validar dados de entrada
- Serializar/deserializar dados para JSON
- Fornecer autocompletion e verificação de tipos
"""

# Modelo básico
class Usuario(SQLModel, table=True):
    # O parâmetro table=True indica que esta classe representa uma tabela
    
    # Por padrão, os campos são obrigatórios
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True)
    idade: Optional[int] = None
    ativo: bool = True
    data_criacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    # O SQLModel herda do Pydantic, então todas as validações do Pydantic funcionam
    # Por exemplo, poderíamos adicionar:
    # email: str = Field(unique=True, regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


#------------------------------------------------------
# 3. Relacionamentos
#------------------------------------------------------
"""
SQLModel suporta os mesmos tipos de relacionamentos que o SQLAlchemy,
mas com uma sintaxe mais limpa e intuitiva.
"""

# Relacionamento um-para-muitos
class Endereco(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rua: str
    cidade: str
    estado: str
    
    # Chave estrangeira
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    
    # No SQLModel, o relacionamento é definido assim:
    usuario: Optional["Usuario"] = Relationship(back_populates="enderecos")


# Atualiza a classe Usuario para incluir o relacionamento reverso
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True)
    idade: Optional[int] = None
    ativo: bool = True
    data_criacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    # Relacionamento reverso
    enderecos: List["Endereco"] = Relationship(back_populates="usuario")


# Note que precisamos atualizar as referências circulares:
SQLModel.update_forward_refs()


#------------------------------------------------------
# 4. Engine e Criação de Tabelas
#------------------------------------------------------
"""
A criação de engines e tabelas no SQLModel é muito similar ao SQLAlchemy,
mas com uma sintaxe mais simplificada.
"""

# Criando o engine
engine = create_engine("sqlite:///database.db", echo=True)

# Criar todas as tabelas
SQLModel.metadata.create_all(engine)


#------------------------------------------------------
# 5. Operações com Session
#------------------------------------------------------
"""
O SQLModel usa o mesmo sistema de sessões do SQLAlchemy, mas com uma API
mais consistente e intuitiva.
"""

# Inserir dados
with Session(engine) as session:
    # Criando um novo usuário
    novo_usuario = Usuario(nome="Maria Silva", email="maria@exemplo.com", idade=30)
    
    # Adicionando à sessão
    session.add(novo_usuario)
    
    # Commit automático ao sair do bloco with (sem exceções)
    # Também faz rollback automático em caso de exceção
    
# Inserir múltiplos registros
with Session(engine) as session:
    usuarios = [
        Usuario(nome="João Santos", email="joao@exemplo.com", idade=25),
        Usuario(nome="Ana Oliveira", email="ana@exemplo.com", idade=28)
    ]
    
    # Adicionando múltiplos registros
    session.add_all(usuarios)
    session.commit()
    
    # Depois de commit, os IDs são preenchidos automaticamente
    for usuario in usuarios:
        print(f"Usuário {usuario.nome} tem ID {usuario.id}")


#------------------------------------------------------
# 6. Consultas (Queries)
#------------------------------------------------------
"""
No SQLModel, as consultas utilizam a nova API de consulta do SQLAlchemy 2.0,
com uma sintaxe mais limpa e intuitiva.
"""

# Consulta básica
with Session(engine) as session:
    # Selecionar todos os usuários
    statement = select(Usuario)
    usuarios = session.exec(statement).all()
    
    # Filtragem simples
    statement = select(Usuario).where(Usuario.nome == "Maria Silva")
    maria = session.exec(statement).first()
    
    # Múltiplas condições
    statement = select(Usuario).where(
        Usuario.ativo == True,
        Usuario.idade > 25
    ).order_by(Usuario.nome)
    usuarios_ativos = session.exec(statement).all()
    
    # Joins
    statement = select(Usuario, Endereco).join(Endereco)
    resultados = session.exec(statement).all()
    for usuario, endereco in resultados:
        print(f"{usuario.nome} mora em {endereco.cidade}-{endereco.estado}")


#------------------------------------------------------
# 7. Atualizações e Exclusões
#------------------------------------------------------
"""
O SQLModel combina a simplicidade do Pydantic para atualizações parciais
com o poder do SQLAlchemy para operações de banco de dados.
"""

# Atualização de registro
with Session(engine) as session:
    # Buscar o usuário
    statement = select(Usuario).where(Usuario.email == "maria@exemplo.com")
    usuario = session.exec(statement).one()
    
    # Atualizar atributos
    usuario.idade = 31
    
    # Salvar as alterações
    session.add(usuario)
    session.commit()
    
    # Verificar a atualização
    usuario_atualizado = session.exec(
        select(Usuario).where(Usuario.id == usuario.id)
    ).one()
    print(f"Idade atualizada: {usuario_atualizado.idade}")

# Exclusão de registro
with Session(engine) as session:
    # Buscar o usuário a ser excluído
    statement = select(Usuario).where(Usuario.email == "joao@exemplo.com")
    usuario = session.exec(statement).one()
    
    # Excluir o usuário
    session.delete(usuario)
    session.commit()
    
    # Verificar a exclusão
    resultado = session.exec(
        select(Usuario).where(Usuario.email == "joao@exemplo.com")
    ).first()
    print(f"Usuário excluído? {'Sim' if resultado is None else 'Não'}")


#------------------------------------------------------
# 8. Modelos de Entrada/Saída
#------------------------------------------------------
"""
Uma das principais vantagens do SQLModel é a capacidade de criar modelos
específicos para entrada (criação) e saída (resposta) de dados,
reutilizando definições e validações.
"""

# Modelo base
class UsuarioBase(SQLModel):
    # Campos compartilhados por todos os modelos derivados
    nome: str
    email: str
    idade: Optional[int] = None

# Modelo para criação (sem ID, que será gerado pelo banco)
class UsuarioCreate(UsuarioBase):
    # Campos específicos para criação
    senha: str  # A senha não será armazenada no modelo de banco

# Modelo para resposta (sem a senha)
class UsuarioRead(UsuarioBase):
    # Inclui o ID que é gerado pelo banco
    id: int
    ativo: bool
    data_criacao: datetime.datetime

# Modelo para banco de dados (completo)
class UsuarioTable(UsuarioBase, table=True):
    # Tabela no banco de dados
    id: Optional[int] = Field(default=None, primary_key=True)
    senha_hash: str  # Armazenamos o hash, não a senha
    ativo: bool = True
    data_criacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# Uso em uma API
def criar_usuario(usuario_data: UsuarioCreate) -> UsuarioRead:
    """
    Função que recebe dados de criação, processa e retorna dados de leitura.
    Idealmente seria usada em uma rota de API (FastAPI, por exemplo).
    """
    with Session(engine) as session:
        # Simula hash de senha
        senha_hash = f"hash_simulado_{usuario_data.senha}"
        
        # Cria o usuário no formato do banco
        db_usuario = UsuarioTable(
            nome=usuario_data.nome,
            email=usuario_data.email,
            idade=usuario_data.idade,
            senha_hash=senha_hash
        )
        
        session.add(db_usuario)
        session.commit()
        session.refresh(db_usuario)
        
        # Converte para o formato de resposta (sem a senha_hash)
        return UsuarioRead(
            id=db_usuario.id,
            nome=db_usuario.nome,
            email=db_usuario.email,
            idade=db_usuario.idade,
            ativo=db_usuario.ativo,
            data_criacao=db_usuario.data_criacao
        )


#------------------------------------------------------
# 9. Migrações com Alembic
#------------------------------------------------------
"""
Para migrações, o SQLModel usa o mesmo Alembic que o SQLAlchemy,
sem alterações significativas na configuração.
"""

# A configuração do Alembic para SQLModel é praticamente idêntica à do SQLAlchemy
# Apenas certifique-se de importar SQLModel em vez de declarative_base

# Exemplo básico de um script de migração para SQLModel:
"""
# migrations/versions/1234567890_criar_tabela_usuarios.py
from alembic import op
import sqlalchemy as sa
import sqlmodel  # Importante importar o sqlmodel

def upgrade():
    op.create_table(
        'usuario',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('idade', sa.Integer()),
        sa.Column('ativo', sa.Boolean(), default=True),
        sa.Column('data_criacao', sa.DateTime())
    )

def downgrade():
    op.drop_table('usuario')
"""


#------------------------------------------------------
# 10. Interação com FastAPI
#------------------------------------------------------
"""
O SQLModel foi projetado para funcionar perfeitamente com o FastAPI,
permitindo criar APIs completas com validação, serialização e 
operações de banco de dados de forma integrada.
"""

# Exemplo de integração com FastAPI
"""
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

app = FastAPI()

# Dependência para obter uma sessão do banco
def get_session():
    with Session(engine) as session:
        yield session

# Rota para criar um usuário
@app.post("/usuarios/", response_model=UsuarioRead)
def create_user(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    # Verificar se o email já existe
    db_usuario = session.exec(
        select(UsuarioTable).where(UsuarioTable.email == usuario.email)
    ).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Criar o usuário
    senha_hash = f"hash_simulado_{usuario.senha}"
    db_usuario = UsuarioTable(
        nome=usuario.nome,
        email=usuario.email,
        idade=usuario.idade,
        senha_hash=senha_hash
    )
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario  # Conversão automática para UsuarioRead

# Rota para buscar todos os usuários
@app.get("/usuarios/", response_model=List[UsuarioRead])
def read_users(session: Session = Depends(get_session)):
    usuarios = session.exec(select(UsuarioTable)).all()
    return usuarios  # Conversão automática para List[UsuarioRead]
"""


#------------------------------------------------------
# 11. Boas Práticas e Dicas
#------------------------------------------------------
"""
Algumas dicas específicas para trabalhar com SQLModel de forma eficiente.
"""

# 1. Use modelos aninhados
class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str

class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    preco: float
    
    # Referência à categoria
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    categoria: Optional[Categoria] = Relationship()
    
    # Validação de preço (como no Pydantic)
    @validator("preco")
    def preco_positivo(cls, v):
        if v <= 0:
            raise ValueError("O preço deve ser positivo")
        return v

# 2. Use transações explícitas para operações complexas
with Session(engine) as session:
    # Inicia uma transação explícita
    with session.begin():
        # Múltiplas operações que devem ser atômicas
        categoria = Categoria(nome="Eletrônicos")
        session.add(categoria)
        
        # A sessão usará refresh para obter o ID gerado
        produtos = [
            Produto(nome="Smartphone", preco=999.99, categoria=categoria),
            Produto(nome="Notebook", preco=1999.99, categoria=categoria)
        ]
        session.add_all(produtos)
        # O commit ocorre automaticamente ao sair do bloco session.begin()

# 3. Trabalhe com migrações desde o início do projeto
# É mais fácil implementar migrações no início do que adaptar um projeto existente

# 4. Configure índices para consultas frequentes
class Artigo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(index=True)  # Adiciona um índice neste campo
    conteudo: str
    data_publicacao: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, 
        index=True  # Índice para consultas por data
    )


#------------------------------------------------------
# 12. Comparação SQLModel vs SQLAlchemy
#------------------------------------------------------
"""
O SQLModel é construído sobre o SQLAlchemy, mas traz algumas vantagens:

1. Integração com Pydantic para validação de dados
2. Modelos unificados para banco de dados e API
3. Suporte nativo a tipagem (menos códigos boilerplate)
4. Sintaxe mais limpa e moderna (baseada em SQLAlchemy 2.0)
5. Integração perfeita com FastAPI
"""

# Mesmo modelo em SQLAlchemy vs SQLModel

# SQLAlchemy:
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UsuarioSQLAlchemy(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    idade = Column(Integer)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
"""

# SQLModel (significativamente mais conciso):
"""
from sqlmodel import SQLModel, Field
import datetime
from typing import Optional

class UsuarioSQLModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True)
    idade: Optional[int] = None
    ativo: bool = True
    data_criacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
"""