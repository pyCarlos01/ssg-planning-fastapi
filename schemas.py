from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):    
    nome: str
    email: str
    senha: str
    admin: Optional[bool]

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ManifestSchema(BaseModel):
    manifest: str
    carrier: str
    cbm: float
    total_pcs: int
    total_amount: float
    ship_type: str
    pgi: str
    pick_to: str
    division: str
    warehouse: str

    class Config:
        from_attributes = True

class DeliverySchema(BaseModel):
    delivery: int
    shipment: str
    customer: str
    city: str
    schedule: str
    uf: str
    total_pcs_del: int

    class Confing:
        from_attributes = True

class WMSSchema(BaseModel):
    driver_name: str
    plate_1: str
    plate_2: str
    gate_in_date: str
    gate_in: str
    dock_in: str
    out_confirm: str
    dock_out: str
    rm_out: str
    gate_out_date: str
    gate_out: str
    status: str
    status_geral: str
    otp: str
    
    class Config:
        from_attributes = True

class ActionSchema(BaseModel):
    alter_pgi: bool
    alter_carrier: bool
    desdobro_total: bool
    desdobro_partial: bool
    failed_check_list: bool
    include_manifest: bool
    obs: str
        
    class Config:
        from_attributes = True

class ResponseSchemaDelivery(BaseModel):
    delivery: int
    shipment: str
    customer: str
    city: str
    schedule: str
    uf: str
    total_pcs_del: int
    action: List[ActionSchema]

    class Confing:
        from_attributes = True

class ResponseSchema(BaseModel):
    manifest: str
    carrier: str
    cbm: float
    total_pcs: int
    total_amount: float
    ship_type: str
    pgi: str
    pick_to: str
    division: str
    warehouse: str
    deliverys: List[ResponseSchemaDelivery]
    wms: List[WMSSchema]
        
    class Config:
        from_attributes = True