'This file uses a in process dictionary for data read and write, not a database. options on the dictionary doesnt follow ACID properties.'

from fastapi import FastAPI, HTTPException
# Fastapi automatically validates all the data incoming and outgoing. so mentioning the data type is a good practice, as fastapi also documents it.
from app.schemas import PostCreate
#we need a way such that the database is created if it doesnt exist when the web server is created.

# ALSO, It is a great practice to return the data type/Schema returned in each fuction for documentation purposes.

server = FastAPI()



text_posts = {
    1: {"title": "New Post", "content": "Cool test post"},
    2: {"title": "Python Tip", "content": "Use list comprehensions for cleaner loops."},
    3: {"title": "Daily Motivation", "content": "Consistency beats intensity every time."},
    4: {"title": "Fun Fact", "content": "The first computer bug was an actual moth found in a Harvard Mark II."},
    5: {"title": "Update", "content": "Just launched my new project! Excited to share more soon."},
    6: {"title": "Tech Insight", "content": "Async I/O in Python can massively speed up I/O-bound tasks."},
    7: {"title": "Quote", "content": "Programs must be written for people to read, and only incidentally for machines."},
    8: {"title": "Weekend Plans", "content": "Might finally clean up my GitHub repos... or just play some Minecraft."},
    9: {"title": "Question", "content": "What's the most underrated Python library you've ever used?"},
    10: {"title": "Mini Announcement", "content": "New video drops tomorrow—covering the weirdest Python features!"}
}
print(len(text_posts))

# we can only return a pydantic object or a python dictionary
@server.get("/health")
def hello_world():
    return {"message":'sab ok hain G'}

#limit is a query parameter
# limit:int = None , making it none makes it optional
@server.get("/posts")
def get_all_posts(limit:int=None):
    if limit:
        if limit<0 or limit>len(text_posts):
            raise HTTPException(detail='Invalid limit provided by the user')
            
        return list(text_posts.values())[:limit]
    return text_posts

#id is a path parameter
@server.get("/posts/{id}")
def get_post(id:int) -> PostCreate:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail='Post not found')
    return text_posts.get(id)


@server.post("/posts")
def create_post(post: PostCreate) -> PostCreate:
    new_post = {"title":post.title, "content":post.content}
    text_posts[max(text_posts.keys()) + 1 ] = new_post
    return new_post