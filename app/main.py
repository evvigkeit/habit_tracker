from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import connect_db as db


templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

'''
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.
We need it here to process CSS files which are connected to the main HTML file.
'''
app.mount("/static", StaticFiles(directory="app/styles"), name="static")

@app.get("/authorization")
def login_page(request: Request):
    return templates.TemplateResponse("authorization/authorization.html",{"request": request})

@app.post("/authorization")
def login(request: Request, username: str = Form(), password: str = Form()):
    user = db.check_user_exist(username, password)
    if user:
        if user['password'] != password:
            return templates.TemplateResponse("authorization/authorization.html",{"request": request, "password_err": 1})  # 1 - wrong password, 2 - user not exists
        return RedirectResponse(f"/authorized/{username}", status_code=303)
    else:
        return templates.TemplateResponse("authorization/authorization.html",{"request": request, "password_err": 2})


@app.get("/registration")
def registration_page(request: Request):
    return templates.TemplateResponse("authorization/registration.html", {"request": request})

@app.post("/registration")
def login(request: Request, username: str = Form(), email: str = Form(), phone: str = Form(), password: str = Form(), ch_password: str = Form()):
    user = db.check_user_exist(username, email, phone)
    if user:
        for k, v in {"username": username, "email": email, "phone": phone}.items():
            if user[k] == v:
                return templates.TemplateResponse("authorization/registration.html",{"request": request, "registration_err": k})

    if password != ch_password:
        return templates.TemplateResponse("authorization/registration.html",{"request": request, "registration_err": "password"})
    db.create_user(username, email, phone, password)
    return RedirectResponse(f"/authorized/{username}", status_code=303)

@app.get("/authorized/{username}")
def authorized_page(request: Request, username: str):
    return templates.TemplateResponse("authorized.html", {"request": request, "username": username})