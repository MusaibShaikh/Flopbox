from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from routers import file_controller, user_controller

from __init__ import config
from middleware import EndpointExecutionTimeLoggingMiddleware

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

if config.profile_endpoints:
    app.add_middleware(EndpointExecutionTimeLoggingMiddleware)

# Include routers
app.include_router(file_controller.router, prefix='/files')
app.include_router(user_controller.router, prefix='/users')

@app.get("/")
async def root() -> str:
    return "Hello, Root!"

handler = Mangum(app)
