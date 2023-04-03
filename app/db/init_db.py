from sqlalchemy.orm import Session

from app import schemas
from app.core.configuration import settings
from app.crud.crud_users import getUser
from app.crud.crud_users import get_by_email
from app.db import base  # noqa: F401


def init_db(db: Session) -> None:

    current_user = get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not current_user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        current_user = getUser.create(db, obj_in=user_in)  # noqa: F841
