from models import Usuario
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from schemas import UsuarioSchema, LoginSchema
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import pegar_sessao, verificar_token
from main import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dict_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not senha == usuario.senha:
        return False
    return usuario

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if not usuario:
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, usuario_schema.senha, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"message": "User created"}
    else:
        raise HTTPException(status_code=400, detail="Email já existente.")
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }
    
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token, 
            "token_type": "Bearer"
            }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }