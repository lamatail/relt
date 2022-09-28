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


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, name, date):
        self.name = name
        self.date = date


class Operation(Base):
    __tablename__ = 'operation'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description: str = ""):
        self.name = name
        self.description = description


class Metric(Base):
    __tablename__ = 'metric'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description: str = ""):
        self.name = name
        self.description = description


class ProfileOperation(Base):
    __tablename__ = 'profile_operation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_profile = Column(Integer)
    id_operation = Column(Integer)
    id_metric = Column(Integer)
    metric_value = Column(String)


class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_profile = Column(Integer, ForeignKey("profile.id"), nullable=True)
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
    id_report = Column(Integer, ForeignKey("report.id"))
    id_operation = Column(Integer, ForeignKey("operation.id"))
    id_metric = Column(Integer, ForeignKey("metric.id"))
    metric_value = Column(String)
    alias = Column(String)
