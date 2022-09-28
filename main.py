from example.generator import generate_data, percentile, load_plan
from metric.metric_table import *
from db.control import *

if __name__ == '__main__':
    df = generate_data()
    sla = pd.Series([184] * 5, index=['test1', 'test2', 'test3', 'test4', 'test5'])

    trm = TableMetric(df, load_plan, ['name'], time_column='time')
    trm.metric('delay', 'int32', 'response_time', func=percentile(90))
    trm.metric('delay', 'int32', 'response_time', func=np.average)
    # trm.sla(sla, 'sla', lambda x, y: (x - y) / y + 1)
    trm.sla(sla, 'sla')
    trm.assemble_data_metric()
    trm.assemble_data_sla('sla')
    print(trm.assemble_data().head(10))

    #add_metric(session, name='response_time')
    #add_operations(['GoPage'])
    report = add_report(session, name='ih', date=datetime.now(), description='hello')
    add_report_operation(session, trm, report.id)
    print(report.id)
    session.close()
    #print(report.__dict__)


