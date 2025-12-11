from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import route_register, route_personalize, route_auth, route_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======= Include Routers =======
app.include_router(route_register.router_regis)
app.include_router(route_auth.router_auth)
app.include_router(route_personalize.router_personalize)
app.include_router(route_ai.router_ai)
