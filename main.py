from fastapi import FastAPI

from server import router as server_router


app = FastAPI()


app.include_router(server_router)
