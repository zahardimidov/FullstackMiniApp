from config import (ADMIN_PASSWORD, ADMIN_SECRET_KEY, ADMIN_USERNAME, DEV_MODE,
                    HOST)
from fastapi import Request
from jinja2 import pass_context
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from src.ext.jwt_token import create_jwt_token, verify_jwt_token
from src.users.models import User, UserRef


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not (username == ADMIN_USERNAME and password == ADMIN_PASSWORD):
            return False

        token = create_jwt_token({
            'key': ADMIN_SECRET_KEY
        })
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        
        data = verify_jwt_token(token)
        if not data:
            return False

        if data.get('key') != ADMIN_SECRET_KEY:
            return False
        return True


authentication_backend = AdminAuth(secret_key="secret")


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]

    form_widget_args_update = dict(
        id=dict(readonly=True), username=dict(readonly=True))

    category = 'Пользователи'
    name = 'Пользователь'
    name_plural = 'Пользователи'


class UserRefAdmin(ModelView, model=UserRef):
    column_list = [UserRef.referral, UserRef.referrer]

    form_widget_args_update = dict(
        id=dict(readonly=True), username=dict(readonly=True))

    category = 'Пользователи'
    name = 'Рефералы'
    name_plural = 'Рефералы'


@pass_context
def my_url_for(context: dict, name: str, /, **path_params) -> str:
    request: Request = context.get("request")
    url = str(request.url_for(name, **path_params))

    if '/admin/statics/' in url and DEV_MODE and 'https' in HOST:
        url = HOST + '/api/admin/statics/' + path_params['path']
        return url

    return url


def init_admin(app, engine):
    admin = Admin(app, engine=engine, base_url='/admin',
                  authentication_backend=authentication_backend)
    admin.templates.env.globals['url_for'] = my_url_for

    admin.add_view(UserAdmin)
    admin.add_view(UserRefAdmin)
