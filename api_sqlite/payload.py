from pydantic import BaseModel


class Auth(BaseModel):
    username: str
    password: str


class Link(BaseModel):
    link: str


class Code(BaseModel):
    question: str
    compiler: str


class Submit(BaseModel):
    course: str
    compiler: str
    question: str
    code: str
