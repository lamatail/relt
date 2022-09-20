from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

profile_operation_table = Table(
    "profile_operation",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id")),
    Column("operation_id", ForeignKey("operation.id")),
)

profile_tag_table = Table(
    "profile_tag",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id")),
    Column("tag_id", ForeignKey("tag.id")),
)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime(timezone=True), nullable=False)
    operation = relationship(
        "Operation", secondary=profile_operation_table, backref="profiles"
    )

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


class Tags(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description: str = ""):
        self.name = name
        self.description = description