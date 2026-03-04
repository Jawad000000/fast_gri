from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from .. import models, schema, oauth2, database
from sqlalchemy.orm import Session
from sqlalchemy import select
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    stmt=select(models.Post).where(models.Post.id == vote.post_id)
    post= db.execute(stmt).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with this id does not exist")




    stmt=select(models.Vote).where(models.Vote.post_id == vote.post_id,
    models.Vote.user_id == current_user.id)
    found_vote=db.execute(stmt).scalar_one_or_none()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="not allowed")
        
        new_vote=models.Vote(post_id = vote.post_id, user_id=current_user.id )
        db.add(new_vote)
        db.commit()
        return {"message": "Succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        db.delete(found_vote)
        db.commit()

        return {"message": "Successfully deleted vote"}       