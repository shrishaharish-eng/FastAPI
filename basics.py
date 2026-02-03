from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title" : "First Post",
     "content" : "First Post",
     "id": 1},
     {"title" : "Second Post",
     "content" : "Second Post",
     "id": 2}
]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
            break

@app.get("/")
async def root():
    return {"message": "Welcome to my API !!!"}

@app.get("/posts")
async def get_posts():
    # return {"data": "This is your post."}
    return {"data": my_posts}


# @app.post("/createposts")
# async def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']} content: {payload['content']}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(payload: Post):
    payload_dict = payload.model_dump()
    payload_dict["id"] = randrange(1, 1000000)
    my_posts.append(payload_dict)
    return {"data": payload_dict}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found !!")
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
    # print(post)
    return {"post detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found !!")
    else:
        my_posts.pop(index)

@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found !!")
    else:
        payload_dict = payload.model_dump()
        payload_dict["id"] = id
        my_posts[index] = payload_dict
        return {"data": payload_dict}
