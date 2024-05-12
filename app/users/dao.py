import datetime

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import async_session_maker
from app.logger import logger


class UserDAO(BaseDAO):
    model = Users

    '''
    UPDATE users
    SET last_login = today date
    WHERE user_id = user_id;
    '''

    @classmethod
    async def refresh_token_for_user(cls, user_id: int):
        try:
            async with async_session_maker() as session:
                refresh_token = (
                    update(Users)
                    .where(Users.id == user_id)
                    .values(last_login=datetime.datetime.now())
                )
                await session.execute(refresh_token)
                await session.commit()


        except (SQLAlchemyError, Exception) as e:

            if isinstance(e, SQLAlchemyError):

                msg = "Database Exc: Cannot add booking"

            elif isinstance(e, Exception):

                msg = "Unknown Exc: Cannot add booking"

            extra = {"user_id": user_id}

            logger.error(msg, extra=extra, exc_info=True)
