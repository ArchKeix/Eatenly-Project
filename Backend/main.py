from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import route_register, route_personalize

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======= Include Routers =======
app.include_router(route_register.router_regis)  # sesuaikan nama router
app.include_router(route_personalize.router_personalize)
