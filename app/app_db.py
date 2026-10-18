'''Actual server that handles CRUD Operations for our main social media app.    '''

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
# Fastapi automatically validates all the data incoming and outgoing. so mentioning the data type is a good practice, as fastapi also documents it.
from app.schemas import PostCreate
from app.db import Post, create_db_and_tables, get_async_session, User
#we need a way such that the database is created if it doesnt exist when the web server is created.
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

from app.images import image_kit
# from imagekitio import ImageKit
import shutil
import os 
import uuid
import tempfile
import asyncio
import logging

from app.users import auth_backend,current_active_user,fastapi_users
from app.schemas import UserRead,UserCreate,UserUpdate
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


# ALSO, It is a great practice to return the data type/Schema returned in each fuction for documentation purposes.

server = FastAPI(lifespan=lifespan)

#in my server, i am including these routes
server.include_router(fastapi_users.get_auth_router(auth_backend),prefix='/auth/jwt',tags=["auth"])
server.include_router(fastapi_users.get_register_router(UserRead, UserCreate),prefix="/auth", tags=["auth"])
server.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags=["auth"])
server.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
server.include_router(fastapi_users.get_users_router(UserRead,UserUpdate),prefix="/users",tags=["users"])


@server.get('/')
async def home():
    return {"message":"this is home"}

## Protecting the endpoints, so now that we have made the authentication setup , the endpoints will first look for the existence of a active user. if it doesnt exist, then it wont simply run

@server.post('/upload', response_model=None)
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    temp_file_path = None
    try:
        suffix = os.path.splitext(file.filename or "")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        def _upload():
            with open(temp_file_path, "rb") as f:
                return image_kit.files.upload(
                    file=f,
                    file_name=file.filename,
                    use_unique_file_name=True,
                    tags=["backend-upload"],
                )

        upload_result = await asyncio.to_thread(_upload)

        post = Post(
            user = user,
            caption=caption,
            url=upload_result.url,
            file_name=upload_result.name,
            file_type="video" if (file.content_type or "").startswith("video/") else "image",
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post

    except Exception as e:
        logger.exception("Upload failed")
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
      


@server.get("/feed")
async def get_feed(
    session : AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),

):
    # we just wrote a query
    result = await session.execute(
    select(Post).order_by(Post.created_at.desc())
    )
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]

    user_dict = {u.id: u.email for u in users}


    posts_data =[]
    for post in posts:
        posts_data.append(
            {
                "id":str(post.id),
                "user_id":str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id==user.id,
                "email":user_dict.get(post.user_id, "Unknown")
            }
        )

    return {"posts": posts_data}

@server.delete("/posts/{post_id}")
async def delete_post(post_id: str, session : AsyncSession = Depends(get_async_session),user: User = Depends(current_active_user)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id== post_uuid))
        post = result.scalars().first() # return exact results rather than whole object

        if not post:
            raise HTTPException(status_code=404,detail="Post not found")

        if post.user_id!=user.id:
            raise HTTPException(status_code=403,detail="You dont have permission to delete this post")
        
        await session.delete(post)
        await session.commit()

        return {"success":True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
