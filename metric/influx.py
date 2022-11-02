import datetime
from influxdb import DataFrameClient


class InfluxV1Exporter():
    def __init__(self,
                 influx_host,
                 influx_port,
                 influx_user,
                 influx_pwd,
                 influx_db):
        self.influx_host = influx_host
        self.influx_port = influx_port
        self.influx_user = influx_user
        self.influx_pwd = influx_pwd
        self.influx_db = influx_db
        self.client = DataFrameClient(host=influx_host, port=influx_port, username=influx_user, password=influx_pwd, database=influx_db)


class JmeterInfluxV1(InfluxV1Exporter):

    def __init__(self, measurement: str = 'script', *args, **kwargs):
        super.__init__(*args, **kwargs)
        self._start_time = None
        self._end_time = None
        self._application = None
        self._measurement = measurement
        self._data = None

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = datetime.strptime(start_time, '%d.%m.%Y %H:%M:%S')

    @property
    def end_time(self):
        return self._end_time

    @start_time.setter
    def end_time(self, end_time):
        self._end_time = datetime.strptime(end_time, '%d.%m.%Y %H:%M:%S')

    @property
    def application(self):
        return self._application

    @start_time.setter
    def application(self, application):
        self._application = application

    def export_metric(self):
        df = self.client.query(f"""select * from {self._measurement} 
                                       from time >= {self._start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')} 
                                       and time < {self._start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')} 
                                       and application = {self._application}""")[self._application]
        dfn = df[(df['transaction'] != 'internal') & (df['transaction'] != 'all') & (df['statut'] != 'all')][
            ['avg', 'count', 'pct90.0', 'pct95.0', 'statut', 'transaction']].dropna(subset=['statut']).fillna(0)
        dfn_ok = dfn[dfn['statut'] == 'ok'].set_index('transaction', append=True)
        dfn_ko = dfn[dfn['statut'] == 'ko'].set_index('transaction', append=True)
        self._data = dfn_ok.join(dfn_ko[['count']], rsuffix='_error').drop(['statut'], axis=1).fillna(0).reset_index().rename(columns={'index': 'time'})
