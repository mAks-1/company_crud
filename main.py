import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.api import router as api_router

app = FastAPI()
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
