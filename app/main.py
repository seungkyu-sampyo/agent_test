from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.thread import thread_router
from app.dispatch import dispatch_router

app = FastAPI(
    title="Agent Test Server",
    version="0.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 도메인 라우터 등록
app.include_router(thread_router)
app.include_router(dispatch_router)
