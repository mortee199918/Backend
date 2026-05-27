
from fastapi import FastAPI
from routes.bubbletea import router as bubbletea_router
from routes.auth import router as auth_router



app = FastAPI(title="Bubble Tea API")
app.include_router(bubbletea_router)
app.include_router(auth_router)


