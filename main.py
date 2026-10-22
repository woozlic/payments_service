from fastapi import FastAPI

from users.routers import router

app = FastAPI()
app.include_router(router)

