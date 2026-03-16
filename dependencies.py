from models import db, Usuario
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from main import SECRET_KEY, ALGORITHM, oatuh2_schema

def pegar_sessao():
    try:
        SESSION = sessionmaker(bind=db)
        session = SESSION()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oatuh2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique validade do token")
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario