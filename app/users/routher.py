import datetime

from fastapi import APIRouter, Depends, Response
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from app.config import settings
from app.exceptions import UserAlreadyExistsException, Credentials
from app.users.auth import (authenticate_user, create_access_token, get_password_hash, create_refresh_token,
                            valid_email_from_db, decode_token)
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserLogin


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_secret,
    client_kwargs={
        'scope': 'email openid profile',
    },
    authorize_state=settings.JWT_SECRET_KEY,
)

FRONTEND_URL = 'https://127.0.0.1:8000/token'


@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(name=user_data.name, email=user_data.email, hashed_password=hashed_password, created_at=datetime.datetime.now(), last_login=datetime.datetime.now())


# @router_auth.post("/login")
# async def login_user(response: Response, user_data: SUserLogin):
#     user = await authenticate_user(user_data.email, user_data.password)
#     access_token = create_access_token({"sub": str(user.id)})
#     response.set_cookie("user_access_token", access_token, httponly=True)
#     return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")


@router_auth.get("/login")
async def login(request: Request):
    url = request.url_for('token')
    return await oauth.google.authorize_redirect(request, url)


@router_auth.get('/token')
async def token(request: Request):
    access_token = await oauth.google.authorize_access_token(request)
    user = access_token.get('userinfo')
    if user:
        request.session['user'] = user
    return user

    # if valid_email_from_db(user_data['email']):
    #     return JSONResponse({
    #         'result': True,
    #         'user_access_token': create_access_token(user_data['email']),
    #         'refresh_token': create_refresh_token(user_data['email']),
    #     })
    # raise Credentials


@router_auth.post('/refresh')
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == 'POST':
            form = await request.json()
            if form.get('grant_type') == 'refresh_token':
                token = form.get('refresh_token')
                payload = decode_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                    email = payload.get('sub')
                    # Validate email
                    if valid_email_from_db(email):
                        # Create and return token
                        return JSONResponse({'result': True, 'access_token': create_access_token(email)})

    except Exception:
        raise Credentials
    raise Credentials


# @app.get('/auth')
# async def auth(request: Request):
#     try:
#         token = await oauth.google.authorize_access_token(request)
#     except OAuthError as e:
#         return templates.TemplateResponse(
#             name='error.html',
#             context={'request': request, 'error': e.error}
#         )
#     user = token.get('userinfo')
#     if user:
#         request.session['user'] = dict(user)
#     return RedirectResponse('welcome')

@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user