import os
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey

db = create_engine(os.getenv("DATABASE_URL"))
BASE = declarative_base()

class Usuario(BASE):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String)
    senha = Column("senha", String)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin

class Manifest(BASE):
    __tablename__ = "manifests"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    manifest = Column("manifest", String)
    carrier = Column("carrier", String)
    cbm = Column("cbm", Float)
    total_pcs = Column("total_pcs", Integer)
    total_amount = Column("total_amount", Float)
    ship_type = Column("ship_type", String)
    pgi = Column("pgi", String)
    pick_to = Column("pick_to", String)
    division = Column("division", String)
    warehouse = Column("warehouse", String)
    deliverys = relationship("Delivery", cascade="all, delete")
    wms = relationship("WMS", cascade="all, delete")

    def __init__(self, manifest, carrier, cbm, total_pcs, total_amount, ship_type, pgi, pick_to, division, warehouse):
        self.manifest = manifest
        self.carrier = carrier
        self.cbm = cbm
        self.total_pcs = total_pcs
        self.total_amount = total_amount 
        self.ship_type = ship_type
        self.pgi = pgi
        self.pick_to = pick_to
        self.division = division
        self.warehouse = warehouse

class Delivery(BASE):
    __tablename__ = "deliverys"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    delivery = Column("delivery", Integer, unique=True)
    shipment = Column("shipment", String)
    customer = Column("customer", String)
    city = Column("city", String)
    schedule = Column("schedule", String)
    uf = Column("uf", String)
    total_pcs_del = Column("total_pcs_del", Integer)
    id_manifest = Column("id_manifest", ForeignKey("manifests.id"))
    action = relationship("Action", cascade="all, delete")

    def __init__(self, delivery, shipment, customer, city, schedule, uf, total_pcs_del, id_manifest):
        self.delivery = delivery
        self.shipment = shipment
        self.customer = customer
        self.city = city
        self.schedule = schedule
        self.uf = uf
        self.total_pcs_del = total_pcs_del
        self.id_manifest = id_manifest

class WMS(BASE):
    __tablename__ = "wms"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    driver_name = Column("driver_name", String, default="-")
    plate_1 = Column("plate_1", String, default="-")
    plate_2 = Column("plate_2", String, default="-")
    gate_in_date = Column("gate_in_date", String, default="-")
    gate_in = Column("gate_in", String, default="-")
    dock_in = Column("dock_in", String, default="-")
    out_confirm = Column("out_confirm", String, default="-")
    dock_out = Column("dock_out", String, default="-")
    rm_out = Column("rm_out", String, default="-")
    gate_out_date = Column("gate_out_date", String, default="-")
    gate_out = Column("gate_out", String, default="-")
    status = Column("status", String)
    status_geral = Column("status_geral", String)
    otp = Column("otp", String)
    id_manifest = Column("id_manifest", ForeignKey("manifests.id"))

    def __init__(self, driver_name, plate_1, plate_2, gate_in_date, gate_in, dock_in, out_confirm, dock_out, rm_out, gate_out_date, gate_out, status, status_geral, otp, id_manifest):
        self.driver_name = driver_name
        self.plate_1 = plate_1
        self.plate_2 = plate_2
        self.gate_in_date = gate_in_date 
        self.gate_in = gate_in
        self.dock_in = dock_in 
        self.out_confirm = out_confirm 
        self.dock_out = dock_out
        self.rm_out = rm_out
        self.gate_out_date = gate_out_date
        self.gate_out = gate_out
        self.status = status
        self.status_geral = status_geral
        self.otp =  otp
        self.id_manifest = id_manifest

class Action(BASE):
    __tablename__ = "actions"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    alter_pgi = Column("alter_pgi", Boolean, default=False) 
    alter_carrier = Column("alter_carrier", Boolean, default=False) 
    desdobro_total = Column("desdobro_total", Boolean, default=False) 
    desdobro_partial = Column("desdobro_partial", Boolean, default=False) 
    failed_check_list = Column("failed_check_list", Boolean, default=False)
    include_manifest = Column("include_manifest", Boolean, default=False) 
    obs = Column("obs", String, default="-")
    id_delivery = Column("id_delivery", ForeignKey("deliverys.id"))

    def __init__(self, alter_pgi, alter_carrier, desdobro_total, desdobro_partial, failed_check_list, include_manifest, obs, id_delivery):
        self.alter_pgi = alter_pgi
        self.alter_carrier = alter_carrier
        self.desdobro_total = desdobro_total
        self.desdobro_partial = desdobro_partial
        self.failed_check_list = failed_check_list
        self.include_manifest = include_manifest
        self.obs = obs
        self.id_delivery = id_delivery


