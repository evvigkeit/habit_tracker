from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/login")
def login_page():
    return FileResponse("frontend/authorization.html")

@app.post("/authorized")
def login(username: str = Form(), password: str = Form()):
    return {"username": username,
            "password": password}