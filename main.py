from fastapi import FastAPI, Depends, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import model
import schema
from database import SessionLocal, engine

app = FastAPI()
model.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/movie", response_class=HTMLResponse)
def read_movies(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(model.Movie).all()
    return templates.TemplateResponse("index.html", {"request": request, "data": records})


@app.get("/movie/{name}", response_class=HTMLResponse)
def read_movie(request: Request, name: schema.Movie.name, db: Session = Depends(get_database_session)):
    item = db.query(model.Movie).filter(model.Movie.id == name).first()
    print(item)
    return templates.TemplateResponse("overview.html", {"request": request, "movie": item})


@app.post("/movie/")
async def create_movie(db: Session = Depends(get_database_session),
                       name: str = Form(...),
                       url: schema.Movie.url = Form(...),
                       rate: schema.Movie.rating = Form(...),
                       type: schema.Movie.type = Form(...),
                       desc: schema.Movie.desc = Form(...)):
    movie = model.Movie(name=name, url=url, rating=rate, type=type, desc=desc)
    db.add(movie)
    db.commit()
    response = RedirectResponse('/movie', status_code=303)
    return response


@app.patch("/movie/{id}")
async def update_movie(request: Request, id: int,
                       db: Session = Depends(get_database_session)):
    req_body = await request.json()
    movie = db.query(model.Movie).get(id)
    movie.name = req_body.get('name')
    movie.desc = req_body.get('desc')
    db.commit()
    db.refresh(movie)
    new_movie = jsonable_encoder(movie)
    return JSONResponse(status_code=200, content={
        'status_code': 200,
        'message': 'Success',
        'movie': new_movie
    })


@app.delete("/movie/{id}")
async def delete_movie(id: int, db: Session = Depends(get_database_session)):
    movie = db.query(model.Movie).get(id)
    db.delete(movie)
    db.commit()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "movie": None
    })
