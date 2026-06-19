from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request

import connect_db as db

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

'''
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.
We need it here to process CSS files which are connected to the main HTML file.
'''
app.mount("/static", StaticFiles(directory="app/styles"), name="static")

@app.get("/authorization")
def login_page(request: Request):
    return templates.TemplateResponse("authorization.html",{"request": request})

@app.get("/registration")
def registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.post("/authorization")
def login(request: Request, username: str = Form(), password: str = Form()):
    user = db.add_user_data(username, password)
    if user and user[1] != password:
        return templates.TemplateResponse("authorization.html",{"request": request, "password_err": True})
    else:
        return RedirectResponse(f"/authorized/{username}", status_code=303)

@app.get("/authorized/{username}")
def authorized_page(request: Request, username: str):
    return templates.TemplateResponse("authorized.html", {"request": request, "username": username})