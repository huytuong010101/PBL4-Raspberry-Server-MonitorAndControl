from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers import file_router, socket_router, appplication_router


# Init app
app = FastAPI()
# Template
templates = Jinja2Templates(directory="templates")

# Include router
app.include_router(socket_router.socket_router)
app.include_router(file_router.file_router, prefix="/files")
app.include_router(appplication_router.app_router, prefix="/apps")

# Home page
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


