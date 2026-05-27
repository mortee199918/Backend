
from fastapi import FastAPI
from routes.bubbletea import router as bubbletea_router
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bubble Tea API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_origin_regex=r"https?://(localhost|127.0.0.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)


app.include_router(bubbletea_router)
app.include_router(auth_router)


