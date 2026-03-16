from typing import List
from sqlalchemy.orm import Session
from services import upsert_manifest
from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from models import Usuario, Manifest, Delivery, Action, WMS
from schemas import ActionSchema, DeliverySchema, ManifestSchema, WMSSchema, ResponseSchema

man_router = APIRouter(prefix="/manifest", tags=["manifest"], dependencies=[Depends(verificar_token)])

@man_router.get("/listar", response_model=List[ResponseSchema])
async def listar_deliverys(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  if not usuario.admin:
    raise HTTPException(status_code=400, detail="Você não tem autorização para fazer essa modificação")
  else:
    # FILTRAR PELO PGI .filter(Manifest.pgi=="14/03/2026").all()
    manifests = session.query(Manifest).all()
    return manifests

@man_router.post("/atualizar")
def create_or_update_manifest(payload: list[ResponseSchema], db: Session = Depends(pegar_sessao)):
    result = upsert_manifest(payload, db)
    return {"status": result}












# CRIAR ROTA PARA ATUALIZAR OS STATUS DAS DELIVERYS
# CRIAR ROTA PARA ATUALIZAR OS MANIFESTOS
# CRIAR ROTA PARA ATUALIZAR O WMS
# CRIAR ROTA PARA ATUALIZAR AS DELIVERYS