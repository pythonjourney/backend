from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException, Response
from typing import Optional

from pydantic import BaseModel

from model import Todo

from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)


class User(BaseModel):
    id: Optional[int]
    name: str
    email: str


app = FastAPI()

origins = ["https://localhost:3000"]

app.add_middleware( CORSMiddleware,
                   
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]





    )


@app.get("/")
async def read_root():
   return {"Hello": "fastapi"}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")

@app.post("/api/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put("/api/todo/{title}/", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {title}")



#@app.get('/course')
#async def course_info():
 #   return {"welcome": "please select cours"}

#path parameter
#parameter with default value
@app.get('/class/{name}')
async def course_enroll(name:str, phoneno:int=9642772136):
    return {"coursename":name, "phoneno":phoneno}

#optional parameter

@app.get('/coursename/{coursename}')
async def course_enroll(coursename:str, phoneno:Optional[int]=None):
    return {"coursename":coursename, "phoneno":phoneno}

@app.post('/users')
async def create_user(user: User):
    return {"message": f"User {user.name} {user.email} created successfully"}

@app.get('/index')
async def index():
  ret='''

 <html>
 <body style="background-color:lightblue;">
<h2> <b>  StatusUpdate.IO </b></h2>

 </body>

 </html>

    '''
  return Response(content=ret, media_type="text/html")

@app.get('/calculate/api')
async def calc(x: int, y: int, z: Optional[int]=None):
    if z == 0:
        raise HTTPException(status_code=400, detail="Z: division by zero error")

    if z is not None:
        value = x+y

    return { 


        'x': x,
        'y': y,
        'z': z,    
        'value': value

    }
    