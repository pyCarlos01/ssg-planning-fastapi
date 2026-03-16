from sqlalchemy.orm import Session
from models import Manifest, Delivery, Action, WMS

def upsert(db, model, data: dict, pk_field: str):

    instance = db.query(model).filter(getattr(model, pk_field) == data[pk_field]).first()

    if instance:

        for key, value in data.items():
            if getattr(instance, key) != value:
                setattr(instance, key, value)

    else:
        instance = model(**data)
        db.add(instance)

    return instance

def upsert_manifest(payload, db: Session):

    for manifest_data in payload:
        manifest = upsert(db,Manifest,manifest_data.dict(exclude={"deliverys", "wms"}), "manifest")

        db.flush()  # garante que manifest.id exista

        for delivery in manifest_data.deliverys:
            delivery_data = delivery.dict(exclude={"action"})
            delivery_data["id_manifest"] = manifest.id
            delivery_obj = upsert(db, Delivery, delivery_data, "delivery")
            db.flush()  # garante delivery.id
            for action in delivery.action:
                action_data = action.dict()
                action_data["id_delivery"] = delivery_obj.id
                upsert(db, Action, action_data, "id_delivery")

        for wms in manifest_data.wms:
            wms_data = wms.dict()
            wms_data["id_manifest"] = manifest.id
            upsert(db, WMS, wms_data, "id_manifest")

    db.commit()

    return len(payload)