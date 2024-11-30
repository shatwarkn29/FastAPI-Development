from fastapi import FastAPI ,Response , status, HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from .. import schemas , database , oauth2 , models


router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/" , status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote , db : Session = Depends(database.get_db) , current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"The post is not present")
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id , models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail=f"User {current_user.id} has already voted on the post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id , user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Vote does not exist")
        vote_query.delete(synchronize_session= False)
        db.commit()

        return {"message":"successfully deleted vote"}