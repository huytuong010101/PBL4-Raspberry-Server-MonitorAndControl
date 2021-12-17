from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import file_router, socket_router, appplication_router, auth_router, user_router, tracking_router


# Init app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Static service
app.mount("/static", StaticFiles(directory="templates"), name="static")
# Include router
app.include_router(socket_router.socket_router)
app.include_router(file_router.file_router, prefix="/files")
app.include_router(appplication_router.app_router, prefix="/apps")
app.include_router(auth_router.auth_router, prefix="/token")
app.include_router(user_router.user_router, prefix="/user")
app.include_router(tracking_router.tracking_router, prefix="/tracking")


# Home page
@app.get("/")
async def home():
    return FileResponse("./templates/index.html")


# Login page
@app.get("/login")
async def home(request: Request):
    return FileResponse("./templates/login.html")

