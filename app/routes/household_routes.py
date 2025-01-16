from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import Household, User
from ..schemas.user import HouseholdCreate, Household as HouseholdSchema
from ..auth.auth0 import auth0_handler

router = APIRouter()

@router.post("/", response_model=HouseholdSchema)
async def create_household(
    household: HouseholdCreate, 
    token: dict = Depends(auth0_handler.verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.auth0_id == token.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db_household = Household(
        name=household.name,
        created_by_id=user.id
    )
    db_household.members.append(user)
    
    db.add(db_household)
    db.commit()
    db.refresh(db_household)
    return db_household

@router.post("/{household_id}/members/{user_id}")
async def add_member(
    household_id: int,
    user_id: int,
    token: dict = Depends(auth0_handler.verify_token),
    db: Session = Depends(get_db)
):
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
        
    new_member = db.query(User).filter(User.id == user_id).first()
    if not new_member:
        raise HTTPException(status_code=404, detail="User not found")
        
    household.members.append(new_member)
    db.commit()
    return {"status": "success"}