from example.generator import generate_data, percentile, load_plan
from metric.analysis import LoadStepMetric
from metric.metric_table import *
from metric.metric import *
from db.control import *


def test():
    df = generate_data()
    sla = pd.Series([184] * 5, index=['test1', 'test2', 'test3', 'test4', 'test5'])
    trm = TableMetric(df, load_plan, ['name'], time_column='time')
    trm.metric('delay', 'int32', 'per90', func=percentile(90))
    # trm.metric('delay', 'int32', 'response_time', func=np.average)
    trm.sla(sla, 'sla')
    trm.assemble_data_metric()
    trm.assemble_data_sla('sla')
    insert_operations(session, [Operation(name=o[0]) for o in trm.operation_name])
    report = insert_report(session, Report('first', datetime.now()))
    add_report_operation(session, trm, report.id)
    session.close()
    print(trm.data_metric_assemble.head())
    return trm


if __name__ == '__main__':
    df = generate_data()
    sm = LoadStepMetric(df, load_plan=load_plan, operation_column=['name'], time_column='time')
    sm.metric('delay', rpm)
    sm.metric('delay', avg)
    print(sm.assemble_data_metric())
    sm1 = LoadStepMetric.build_load_metric(sm.assemble_data_metric())
    print(sm1.assemble_data_metric())
