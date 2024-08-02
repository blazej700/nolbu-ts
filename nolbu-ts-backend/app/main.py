from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from app.dependencies import ***
#from app.internal import ***
from app.routers import nolbu_ts

app = FastAPI()

origins = [
    "http://68.183.78.107:10001",
    "http://68.183.78.107:10002",
    "http://68.183.78.107:80",
    "http://localhost:3080",
    "http://049945.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "HEAD", "PUT"],
    allow_headers=["Origin", "X-Requested-With, Content-Type, Accept"],
    expose_headers=["content-disposition"]
)

app.include_router(nolbu_ts.router)
