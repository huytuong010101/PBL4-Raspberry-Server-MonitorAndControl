from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers import *


# Init app
app = FastAPI()
# Template
templates = Jinja2Templates(directory="templates")

# Include router
app.include_router(socket_router.socket_router)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


