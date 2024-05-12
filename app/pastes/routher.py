import datetime

from fastapi import APIRouter, Depends, Response, Form
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.config import settings
# from app.exceptions import
from app.pastes.dao import PastesDAO
from app.pastes.models import Pastes
from app.pastes.schemas import SPastes

router_pastes = APIRouter(
    prefix="/pastes",
    tags=["Pastes"],
)


@router_pastes.post("/send", status_code=201)
async def create_paste(paste: SPastes):
    return paste
