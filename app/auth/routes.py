from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth.utils import hash_password
from app.auth.jwt_handler import create_access_token,create_refresh_token
from app.auth.utils import verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.deps import get_current_user, get_current_admin
from fastapi import Body
from app import config
from fastapi import Path
from jose import JWTError, jwt


router = APIRouter(prefix="/auth", tags=["Auth"])

# ✅ Rota de registro
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    hashed_pw = hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Rota de login
@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Rota de refresh token
@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido ou expirado"
    )

    try:
        payload = jwt.decode(refresh_token.refresh_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        if payload.get("type") != "refresh":
            raise credentials_exception
        user_id = int(payload.get("sub"))
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise credentials_exception

    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# Rota para usuários logados
@router.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Olá, {current_user.email}! Você acessou uma rota protegida."}

# Rota exclusiva para Admins
@router.get("/admin/protected")
def admin_route(current_user: models.User = Depends(get_current_admin)):
    return {"message": f"Olá, Admin {current_user.email}! Você acessou uma rota exclusiva para administradores."}

# Rota para promover outro usuário a Admin
@router.patch("/admin/promote/{user_id}")
def promote_user_to_admin(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    user.is_admin = True
    db.commit()
    db.refresh(user)

    return {"message": f"Usuário {user.email} promovido a administrador com sucesso!"}