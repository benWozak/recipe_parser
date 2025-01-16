from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, User as UserSchema
from ..auth.auth0 import auth0_handler

router = APIRouter()

@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        auth0_id=user.auth0_id,
        email=user.email,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserSchema)
async def read_user_me(token: dict = Depends(auth0_handler.verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.auth0_id == token.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user