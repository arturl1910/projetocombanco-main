# ============================================================
# rotas/clientes.py — CRUD de Clientes
# Descrição: Endpoints para gerenciar os clientes do estúdio.
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import conectar

router = APIRouter()

# Modelo de dados — define os campos que o cliente deve ter
class Cliente(BaseModel):
    nome: str                       # obrigatório
    cpf: str                        # obrigatório
    email: Optional[str] = None     # opcional
    telefone: Optional[str] = None  # opcional

# GET /clientes — lista todos os clientes cadastrados
@router.get("")
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

# GET /clientes/{id} — busca um cliente específico pelo ID
@router.get("/{id}")
def buscar_cliente(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    if not cliente:
        return {"erro": "Cliente não encontrado"}
    return cliente

# POST /clientes — cadastra um novo cliente
@router.post("")
def criar_cliente(cliente: Cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cliente (nome, cpf, email, telefone) VALUES (%s, %s, %s, %s)",
        (cliente.nome, cliente.cpf, cliente.email, cliente.telefone)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Cliente cadastrado com sucesso"}

# PUT /clientes/{id} — atualiza os dados de um cliente existente
@router.put("/{id}")
def atualizar_cliente(id: int, cliente: Cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cliente SET nome=%s, cpf=%s, email=%s, telefone=%s WHERE idcliente=%s",
        (cliente.nome, cliente.cpf, cliente.email, cliente.telefone, id)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Cliente atualizado com sucesso"}

# DELETE /clientes/{id} — exclui um cliente do sistema
@router.delete("/{id}")
def deletar_cliente(id: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cliente WHERE idcliente = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Cliente deletado com sucesso"}
    except Exception as erro:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir este cliente. Verifique se existem agendamentos vinculados a ele."}