# ============================================================
# rotas/senioridade.py — CRUD de Senioridade
# Descrição: Endpoints para gerenciar os níveis de senioridade
#            dos tatuadores (Júnior, Pleno, Sênior, Master...).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from database import conectar

router = APIRouter()

# Modelo de dados — define os campos que a senioridade deve ter
class Senioridade(BaseModel):
    nome: str    # obrigatório — ex: "Júnior", "Pleno", "Sênior"

# GET /senioridade — lista todos os níveis de senioridade
@router.get("")
def listar_senioridade():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM senioridade")
    senioridades = cursor.fetchall()
    conn.close()
    return senioridades

# GET /senioridade/{id} — busca um nível de senioridade pelo ID
@router.get("/{id}")
def buscar_senioridade(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM senioridade WHERE idsenioridade = %s", (id,))
    senioridade = cursor.fetchone()
    conn.close()
    if not senioridade:
        return {"erro": "Senioridade não encontrada"}
    return senioridade

# POST /senioridade — cadastra um novo nível de senioridade
@router.post("")
def criar_senioridade(senioridade: Senioridade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO senioridade (nome) VALUES (%s)", (senioridade.nome,))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade cadastrada com sucesso"}

# PUT /senioridade/{id} — atualiza um nível de senioridade existente
@router.put("/{id}")
def atualizar_senioridade(id: int, senioridade: Senioridade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE senioridade SET nome=%s WHERE idsenioridade=%s", (senioridade.nome, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade atualizada com sucesso"}

# DELETE /senioridade/{id} — exclui um nível de senioridade
@router.delete("/{id}")
def deletar_senioridade(id: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM senioridade WHERE idsenioridade = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Senioridade deletada com sucesso"}
    except Exception as erro:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir esta senioridade. Verifique se algum tatuador está vinculado a ela."}