import influx


class InfluxV1Exporter():
    def __init__(self,
                 influx_host,
                 influx_port,
                 influx_user,
                 influx_pwd,
                 influx_measurement):
        self.influx_host = influx_host
        self.influx_port = influx_port
        self.influx_user = influx_user
        self.influx_pwd = influx_pwd
        self.influx_measurement = influx_measurement


class JmeterInfluxV1(InfluxV1Exporter):

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def export(self):
         pass
