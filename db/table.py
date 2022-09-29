from datetime import datetime
from typing import Any

from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

profile_tag_table = Table(
    "profile_tag",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id")),
    Column("tag_id", ForeignKey("tag.id")),
)

operation_tag_table = Table(
    "operation_tag",
    Base.metadata,
    Column("operation_id", ForeignKey("operation.id")),
    Column("tag_id", ForeignKey("tag.id")),
)

report_tag_table = Table(
    "report_tag",
    Base.metadata,
    Column("report_id", ForeignKey("report.id")),
    Column("tag_id", ForeignKey("tag.id")),
)


class Operation(Base):
    __tablename__ = 'operation'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name
        for field, value in kwargs.items():
            if self.__class__.__dict__[field] and field != 'id':
                self.__setattr__(field, value)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name
        for field, value in kwargs.items():
            if self.__class__.__dict__[field] and field != 'id':
                self.__setattr__(field, value)


class Metric(Base):
    __tablename__ = 'metric'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name
        for field, value in kwargs.items():
            if self.__class__.__dict__[field] and field != 'id':
                self.__setattr__(field, value)

    def __repr__(self) -> str:
        return f"Metric('{self.id}', '{self.name}', '{self.description}')"


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    date = Column(DateTime(timezone=True))
    description = Column(String)

    def __init__(self, name: str, date: datetime, **kwargs: Any) -> None:
        self.name = name
        self.date = date
        for field, value in kwargs.items():
            if self.__class__.__dict__[field] and field != 'id':
                self.__setattr__(field, value)


class ProfileOperation(Base):
    __tablename__ = 'profile_operation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_profile = Column(Integer, ForeignKey("profile.id"), nullable=False)
    id_operation = Column(Integer, ForeignKey("operation.id"), nullable=False)
    id_metric = Column(Integer, ForeignKey("metric.id"), nullable=False)
    metric_value = Column(String, nullable=False)

    def __init__(self, **kwargs: Any) -> None:
        for field, value in kwargs.items():
            if self.__class__.__dict__[field] and field != 'id':
                self.__setattr__(field, value)


class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_profile = Column(Integer, ForeignKey("profile.id"))
    name = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    description = Column(String)

    def __init__(self, name: str, date: datetime, **kwargs: Any) -> None:
        self.name = name
        self.date = date
        for field, value in kwargs.items():
            if self.__class__.__dict__[field] and field != 'id':
                self.__setattr__(field, value)


class ReportOperation(Base):
    __tablename__ = 'report_operation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_report = Column(Integer, ForeignKey("report.id"), nullable=False)
    id_operation = Column(Integer, ForeignKey("operation.id"), nullable=False)
    id_metric = Column(Integer, ForeignKey("metric.id"), nullable=False)
    metric_value = Column(String, nullable=False)
    alias = Column(String)

    def __init__(self, **kwargs: Any) -> None:
        for field, value in kwargs.items():
            if self.__class__.__dict__[field] and field != 'id':
                self.__setattr__(field, value)
