import uvicorn

from fastapi_app.main import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("loader:app", reload=True)