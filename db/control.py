from typing import Union

import pandas as pd
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.table import *
from metric.metric_table import TableMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/postgres', connect_args={'options': '-csearch_path={}'.format('lt')})
session = sessionmaker(engine)()

DEFAULT_METRICS = [

]


def add_operations(session, operations: list[str]):
    session.add_all([Operation(name, description="") for name in set(operations) - set([o[0] for o in session.query(Operation.name)])])
    logger.info(f'Add new operation {set(operations) - set(session.query(Operation.name))} in table Operation')
    session.commit()


def create_tables():
    None


def delete_tables():
    None


def add_metric(session, name: str, description: str = ''):
    metric = Metric(name=name, description=description)
    session.add(metric)
    session.commit()
    return metric


def add_report(session, name: str, date=datetime, description: str = ''):
    report = Report(name=name, date=date, description=description)
    session.add(report)
    session.commit()
    return report


def remove_report(session, id_report: int):
    session.query(Report).filter(Report.id == id_report).delete()
    session.commit()


def add_report_operation(session, table_metric: TableMetric, id_report):
    add_operations(session, [o[0] for o in table_metric.operation_name])
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
            # if not profile_name is None:
            #     if session.query(Profile).filter(Profile.name == profile_name).exists():
            #         report.id_profile = session.query(Profile).filter(Profile.name == profile_name).one().id
            #     else:
            #         logger.warning(f'Not found id profile with name {profile_name} in table Profile')
            #         session.rollback()
            #         raise ValueError(f'Not found id profile with name {profile_name} in table Profile')
            # else:
            #     logger.warning(f'Not set profile')
            query = session.query(Operation).filter(Operation.name == operation)
            if query.first():
                report.id_operation = query.one().id
            else:
                session.rollback()
            session.add(report)
    session.commit()


def get_report(report_name: Union[str, int]) -> TableMetric:
    table_metric = TableMetric()
    session = sessionmaker(engine)()
    if isinstance(report_name, int):
        id_report = session.query(ReportOperation).filter(ReportOperation.id_report == report_name).one()
    elif isinstance(report_name, str):
        session.query(ReportOperation).filter(ReportOperation.id_report == report_name)
    report = session.query(ReportOperation).filter(ReportOperation.id_report == id_report).all()
    alias = set([r.alias for r in report])
    logger.info(f'Report {report_name} have alias {alias}')