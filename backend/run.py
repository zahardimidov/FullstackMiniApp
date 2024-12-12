from bot import process_update, run_bot_webhook
from config import PORT, WEBHOOK_PATH
from database.admin import init_admin
from database.session import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from src.ext.schemas import ErrorResponse
from src.users.api import router as users_router


async def on_startup(app: FastAPI):
    init_admin(app=app, engine=engine)
    await run_database()
    await run_bot_webhook()

    yield

app = FastAPI(lifespan=on_startup, responses={
    400: {"model": ErrorResponse}
})
app.add_api_route('/'+WEBHOOK_PATH, endpoint=process_update,
                  methods=['post'], include_in_schema=False)
app.include_router(users_router)

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
async def home(request):
    return f'<div style="display: flex; width: 100vw; height: 100vh; justify-content: center; background-color: #F9F9F9; color: #03527E;"> <b style="margin-top:35vh">Welcome!</b> </div>'


def prettify_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            parts = route.path.lstrip('/').split('/')
            route.operation_id = parts[0] + \
                ''.join(part.capitalize() for part in parts[1:])


prettify_operation_ids(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, forwarded_allow_ips='*')
