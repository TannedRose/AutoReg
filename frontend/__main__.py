from fastapi import FastAPI, Path
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from src.settings import settings

app = FastAPI()

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=("*",),
    allow_methods=("*",),
    allow_headers=("*",),

)
app.add_middleware(
    middleware_class=ProxyHeadersMiddleware,
    trusted_hosts=("*", )
)
templating = Jinja2Templates(directory=settings.BASE_DIR / "templates")


@app.get(path="/register", name="register")
async def register(request: Request):
    return templating.TemplateResponse(
        request=request,
        name="frontend/register.html",
    )


@app.get(path="/login", name="login")
async def login(request: Request):
    return templating.TemplateResponse(
        request=request,
        name="frontend/login.html",
    )

if __name__ == "__main__":
    from uvicorn import run
    run(app=app, host=settings.HOST, port=settings.PORT)