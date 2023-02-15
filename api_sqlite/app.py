from fastapi import FastAPI, Depends, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import models
from db.database import engine, SessionLocal
from mod.answer import get_answer
from mod.update import add_login_details, update_login_details
from payload import Auth, Link, Code, Submit
from mod.login import app_login, error_login
from mod.scrap import scrap_lang, scrap_level, scrap_question, scrap_read
from mod.submit import submit_code

app = FastAPI()

origin = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origin,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie"],
)
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def no_user_id():
    return {
        "status": "error",
        "message": "user_id token not found please login again",
    }


def template(user_id, func, item, db, name):
    if user_id is None:
        return no_user_id()
    dat = func(db, user_id, item)
    if dat == "logged out":
        db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
        db_user.logged_in = False
        db.commit()
        db.refresh(db_user)
        return {
            "status": "error",
            "message": "Logged out",
        }
    return {
        "status": "success",
        "message": name,
        "data": dat,
    }


@app.get("/admin")
def reveal(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/login")
def log_user(response: Response, auth: Auth, db: Session = Depends(get_db)):
    ur_name = auth.username
    pwd = auth.password
    ses, u = app_login(ur_name, pwd)
    check = 'window.location.href = "http://buildit.iare.ac.in/"'
    db_user = db.query(models.User).filter(models.User.username == auth.username).first()
    if check in u:
        if db_user:
            if not db_user.logged_in:
                update_login_details(ses, db, db_user)
        else:
            add_login_details(ses, db, models)
            db_user = db.query(models.User).filter(models.User.username == auth.username).first()
        uid = db_user.user_id
        response.set_cookie(key="user_id", value=uid)
        return {
            "status": "success",
            "message": "Logged in successfully",
            "url": "/user"
        }
    else:
        if db_user:
            db_user.logged_in = False
            db.commit()
            db.refresh(db_user)
        msg = error_login(u)
        return {
            "status": "error",
            "message": msg,
        }


@app.post("/compiler")
def compiler(user_id: str = Cookie(None)):
    if user_id is None:
        return no_user_id()
    lang = scrap_lang()
    return {
        "status": "success",
        "message": "Compiler list",
        "data": lang
    }


@app.post("/level")
def level(link: Link, user_id: str = Cookie(None), db: Session = Depends(get_db)):
    return template(user_id, scrap_level, link.link, db, "levels list")


@app.post("/question")
def question(link: Link, user_id: str = Cookie(None), db: Session = Depends(get_db)):
    return template(user_id, scrap_question, link.link, db, "question list")


@app.post("/read")
def question(link: Link, user_id: str = Cookie(None), db: Session = Depends(get_db)):
    return template(user_id, scrap_read, link.link, db, "problem statement")


@app.post("/answer")
def answer(code: Code, user_id: str = Cookie(None), db: Session = Depends(get_db)):
    return template(user_id, get_answer, code, db, "answer searched")


@app.post("/submit")
def submit(sub: Submit, user_id: str = Cookie(None), db: Session = Depends(get_db)):
    return template(user_id, submit_code, sub, db, "answer submitted")


@app.post("/logout")
def logout(user_id: str = Cookie(None), db: Session = Depends(get_db)):
    if user_id is None:
        return no_user_id()
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db_user.logged_in = False
    db.commit()
    db.refresh(db_user)
    return {
        "status": "success",
        "message": "Logged out",
    }


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# import uvicorn

# if __name__ == "__main__":
#    uvicorn.run("main:app", port=8080)
