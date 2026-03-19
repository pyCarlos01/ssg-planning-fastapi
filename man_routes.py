import pytz

from typing import List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from services import upsert_manifest
from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from models import Usuario, Manifest, Delivery, Action, WMS
from schemas import ActionSchema, DeliverySchema, ManifestSchema, WMSSchema, ResponseSchema

man_router = APIRouter(prefix="/manifest", tags=["manifest"], dependencies=[Depends(verificar_token)])
fuso = pytz.timezone("America/Sao_Paulo")
today = datetime.now(fuso).strftime("%d/%m/%Y")


@man_router.get("/listar", response_model=List[ResponseSchema])
async def listar_deliverys(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  if not usuario.admin:
    raise HTTPException(status_code=400, detail="Você não tem autorização para fazer essa modificação")
  else:
    manifests = session.query(Manifest).filter(Manifest.pgi==today).all()
    return manifests

@man_router.post("/atualizar")
def create_or_update_manifest(payload: list[ResponseSchema], db: Session = Depends(pegar_sessao)):
    result = upsert_manifest(payload, db)
    return {"status": result}

@man_router.get("/atrasos")
async def get_late_arrival(session: Session = Depends(pegar_sessao)):
  smt = select(
      Manifest.manifest,
      Manifest.carrier,
      Manifest.pick_to,
      WMS.gate_in_date,
      WMS.gate_in,
      WMS.otp,
      Manifest.warehouse
    ).join(
      WMS, WMS.id_manifest == Manifest.id
    ).where(
      Manifest.pgi==today,
      WMS.otp.in_(["WAIT TRUCK DELAYED", "TRUCK ARRIVED DELAYED"])
    )

  late_arrival = session.execute(smt).mappings().all()
  return(late_arrival)
