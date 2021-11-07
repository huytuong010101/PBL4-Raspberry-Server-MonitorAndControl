from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import file_router, socket_router, appplication_router, auth_router, user_router


# Init app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Template
templates = Jinja2Templates(directory="templates")

# Include router
app.include_router(socket_router.socket_router)
app.include_router(file_router.file_router, prefix="/files")
app.include_router(appplication_router.app_router, prefix="/apps")
app.include_router(auth_router.auth_router, prefix="/token")
app.include_router(user_router.user_router, prefix="/user")


# Home page
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


