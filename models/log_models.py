from . import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from .stage_models import created_at, updated_at , intpk


# from app.database import


class LoginAuditOrm(Base):
    __tablename__ = "LoginAudit"

    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[intpk]
    login: Mapped[Optional[str]]
    system_name: Mapped[Optional[str]]
    ip: Mapped[Optional[str]]
    event_type: Mapped[Optional[str]]
    event_name: Mapped[Optional[str]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# class ExcelServiceLogsOrm(Base):
#     __tablename__ = "ExcelServiceLogs"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     # id: Mapped[intpk]
#     error_desc: Mapped[str]
#     path_to_file: Mapped[str]
#     app_name: Mapped[Optional[str]]
#     sys_error_desc: Mapped[str]
#     # createdAt: Mapped[created_at]
#     # updatedAt: Mapped[updated_at]
