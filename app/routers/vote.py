from sys import prefix
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from .. import schema,database,models,oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix='/votes', tags = ['Votes'])


@router.get('/')
def vote(vote: schema.Vote, curret_user : int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db) ):
    post =db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This post {vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == curret_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"This user id {curret_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = curret_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "Your vote has been added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"This vote does not exist")
        vote_query.delete(synchronize_session = False)    
        db.commit()
        return {"message" : "Vote has been deleted"}