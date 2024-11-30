from fastapi import FastAPI ,Response , status, HTTPException , Depends , APIRouter
from .. import models , schemas , utils , oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional , List
from sqlalchemy import func 



router = APIRouter(
    prefix="/posts",
    tags= ['posts']
)

@router.get("/" , response_model= List[schemas.Post_out])
# @router.get("/")
def posts(db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user) ,limit :int=10 ,
          skip : int = 0 , search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post , func.count(models.Votes.post_id).label("votes")).join(models.Votes , models.Votes.post_id == models.Post.id ,isouter=True ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results = list ( map (lambda x : x._mapping, results) )
    posts = [
        {
            "post": post,  # This matches the "post" field in Post_out
            "votes": votes,  # This matches the "votes" field in Post_out
        }
        for post, votes in posts
    ]
    return posts



@router.post("/" , status_code=status.HTTP_201_CREATED , response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate , db : Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) 
    # RETURNING * """ ,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(post.dict())
    print(current_user.id)
    # print(current_user.email)
    create_post = models.Post(owner_id = current_user.id ,**post.dict())
    db.add(create_post)
    db.commit()
    db.refresh(create_post)
    return create_post
# Title :str , Content : str 
# , response_model=List[schemas.Post_out]
@router.get("/{id}" )
def get_post(id: int , db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """ , (str(id),))
    # my_post = cursor.fetchone()
    # print(my_post)
    print(current_user.email)
    # getpost = db.query(models.Post).filter(models.Post.id == id).first()
    getpost = db.query(models.Post , func.count(models.Votes.post_id).label("votes")).join(models.Votes , models.Votes.post_id == models.Post.id ,isouter=True ).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(getpost)
    if not getpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'post with id {id} was not found')
    # getpost = [
    #     {
    #         "post": post,  # This matches the "post" field in Post_out
    #         "votes": votes,  # This matches the "votes" field in Post_out
    #     }
    #     for post, votes in getpost
    # ]
    # return posts
    return getpost


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id: int , db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" , (str(id),))
    # del_post = cursor.fetchone()
    # conn.commit()
    del_post = db.query(models.Post).filter(models.Post.id == id)
    delpost = del_post.first()
    if delpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with id {id} does not exist")
    if delpost.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the required action")
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}" , response_model= schemas.PostResponse)
def updatepost(id:int,updated_post:schemas.PostUpdate , db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s ,content=%s,published=%s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()
    if post_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with the id {id} does not exist")
    if post_data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the required action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

