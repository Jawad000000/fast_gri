from .. import models, schema, utils
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select

router = APIRouter()



@router.post("/signin", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    hased_password=utils.hash_password(user.password)
    user.password=hased_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/users/{id}", response_model=schema.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    stmt=select(models.User).where(models.User.id==id)
    user=db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} was not found")
    return user
