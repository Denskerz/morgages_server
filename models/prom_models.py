from . import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from .stage_models import created_at, updated_at


# from app.database import intpk


class UserOrm(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    # id: Mapped[intpk]
    username: Mapped[str]
    firstname: Mapped[Optional[str]]
    surname: Mapped[Optional[str]]
    lastname: Mapped[Optional[str]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


class RoleOrm(Base):
    __tablename__ = "Role"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_name: Mapped[str]
    name: Mapped[Optional[str]]
    ldap_name: Mapped[Optional[str]]
    ldap_group: Mapped[Optional[str]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]
