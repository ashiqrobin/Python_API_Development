import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from time import sleep


app = FastAPI()

class Post(BaseModel):
    title: str = None
    content: str = None
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', 
        user='postgres', password='app', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        sleep(2)


# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id":1}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"]== id:
#             return p

# def find_index_post(id:int):
#     for i, p in enumerate(my_posts):
#         if p['id']==id:
#             return i
    

@app.get("/")
def root():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    print(posts)
    return posts


@app.get("/posts")
def get_post():
    return {"data": "This is your  post"}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                    (post.title, post.content, post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}


# @app.get("/posts/latest")
# def get_latest_post():
#     latest_posts=my_posts[len(my_posts)-1]
#     return {"latest": latest_posts}


@app.get("/posts/{id}")
def get_posts(id:int):
    print(type(id))
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"Post with: {id} was not found")
    return {"post_data": post}


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"Post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s  RETURNING *""", 
    (post.title,post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"Post with id {id} does not exist")

    return {'data': updated_post}

  




# title str, content str, category, Boolean

