from typing import Union

import pandas as pd
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from db.table import *
from metric.metric_table import TableMetric
from psycopg2 import errors

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/postgres', connect_args={'options': '-csearch_path={}'.format('lt')})
session = sessionmaker(engine)()

DEFAULT_METRICS = [
    Metric(name='avg', description='среднее время обработки запроса'),
    Metric(name='std.dev', description='срендеквадратичное отклоние времени обработки запроса'),
    Metric(name='per90', description='90 персентиль времени обработки запроса'),
    Metric(name='per95', description='95 персентиль времени обработки запроса'),
    Metric(name='rps', description='количество запросов в секунду'),
    Metric(name='rpm', description='количество запросов в минуту'),
    Metric(name='rp5m', description='количество запросов в 5 минту'),
    Metric(name='rp10m', description='количество запросов в 10 минут'),
    Metric(name='rph', description='количество запросов в час')
]


def insert_row(session, obj: Union[Metric, Operation, Profile, Report]) -> Union[Metric, Operation, Profile, Report]:
    try:
        session.add(obj)
        session.commit()
        logger.info(f'Added new {obj} to the table {obj.__tablename__}')
    except exc.IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, errors.UniqueViolation):
            logger.warning(f'The {obj} is already in the table {obj.__tablename__}')
        else:
            raise e
    return obj


def insert_metric(session, metric: Metric) -> Metric:
    return insert_row(session, metric)


def insert_operation(session, operation: Operation) -> Operation:
    return insert_row(session, operation)


def insert_profile(session, profile: Profile) -> Profile:
    return insert_row(session, profile)


def insert_report(session, report: Report) -> Report:
    return insert_row(session, report)


def fill_default_metric(session) -> list[Metric]:
    for metric in DEFAULT_METRICS:
        insert_metric(session, metric)
    return DEFAULT_METRICS


def insert_operations(session, operations: list[Operation]):
    operations_table = session.query(Operation.name).all()
    operations_insert = []
    for operation in list(set(operations) - set(operations_table)):
        operations_insert.append(insert_operation(session, operation))
    return operations_insert


def create_tables():
    None


def delete_tables():
    None


def add_report_operation(session, table_metric: TableMetric, id_report):
    for alias in table_metric.get_alias_level():
        for operation, value in table_metric.data_metric[alias].items():
            report = ReportOperation()
            report.alias = alias
            report.metric_value = value
            report.id_report = id_report
            query = session.query(Metric).filter(Metric.name == table_metric.metric_name)
            if query.first():
                report.id_metric = query.one().id
            else:
                logger.error(f'Not found id metric with name {table_metric.metric_name} in table Metric')
                session.rollback()
                raise ValueError(f'Not found id metric with name {table_metric.metric_name} in table Metric')
            query = session.query(Operation).filter(Operation.name == operation)
            if query.first():
                report.id_operation = query.one().id
            else:
                logger.warning(f'Not found id operation with name {operation} in table Operation')
                session.rollback()
                raise ValueError(f'Not found id operation with name {operation} in table Operation')
            session.add(report)
    session.commit()


def build_table_metric(session, report_name: Union[str, int]) -> TableMetric:
    if isinstance(report_name, int):
        id_report = session.query(Report).filter(Report.id == report_name).one().id
    elif isinstance(report_name, str):
        id_report = session.query(Report).filter(Report.name == report_name).one().id
    report = session.query(Operation.name.label("operation"), Metric.name.label("metric"), ReportOperation.metric_value, ReportOperation.alias).filter(
        Report.id == id_report
    ).filter(
        ReportOperation.id_report == Report.id
    ).filter(
        ReportOperation.id_operation == Operation.id
    ).filter(
        ReportOperation.id_metric == Metric.id
    ).all()
    logger.info(f'Report {report_name} download')
    return pd.pivot_table(pd.DataFrame(report), values='metric_value', index='operation', columns=['alias', 'metric'])
