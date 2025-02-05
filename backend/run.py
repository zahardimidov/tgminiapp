from api.routers import router
from bot import process_update, run_bot_webhook
from config import *
from database.admin import Admin
from database.session import *
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse


async def on_startup(app: FastAPI):
    await run_bot_webhook()
    yield await run_database()

app = FastAPI(lifespan=on_startup)
admin = Admin()


@app.get("/ping", status_code=200)
def ping():
    return {"status": "ok"}


admin.init(app=app, engine=engine)
app.add_api_route(WEBHOOK_PATH, endpoint=process_update, methods=['post'])
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def home():
    return f'<div style="display: flex; width: 100vw; height: 100vh; justify-content: center; background-color: #F9F9F9; color: #03527E;"> <b style="margin-top:35vh">Welcome!</b> </div>'


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = str(exc._errors[0].get('ctx', {}).get('error')) or 'Ошибка валидации'
    return JSONResponse(status_code=422, content=jsonable_encoder({"status": 'error', "message": message}))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder({"status": 'error', "message": exc.detail}))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, forwarded_allow_ips='*')
