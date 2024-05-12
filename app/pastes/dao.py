import datetime

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.pastes.models import Pastes
from app.database import async_session_maker
from app.logger import logger


class PastesDAO(BaseDAO):
    model = Pastes

