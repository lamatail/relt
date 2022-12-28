import os
from flask import Flask, request, jsonify

from db.control import insert_operations, insert_report, add_report_operation, session
from db.table import *
from metric.analysis import LoadStepMetric
from metric.influx import JmeterInfluxV1
from metric.metric import rpm, avg

app = Flask(__name__)

TDB_LT_HOST = os.environ['lt_tdb_host']
TDB_LT_PORT = os.environ['lt_tdb_port']
TDB_LT_USER = os.environ['lt_tdb_user']
TDB_LT_PWD = os.environ['lt_tdb_pwd']
TDB_LT_INST = os.environ['lt_tdb_db']

TDB_PROD_HOST = os.environ['stats_tdb_host']
TDB_PROD_PORT = os.environ['stats_tdb_port']
TDB_PROD_USER = os.environ['stats_tdb_user']
TDB_PROD_PWD = os.environ['stats_tdb_pwd']
TDB_PROD_INST = os.environ['stats_tdb_db']


@app.route("/load/export/influx", methods=['POST'])
def generate_report():
    if request.method == 'POST':
        req_json = request.json
        uid = req_json['uid']
        report_name = req_json['name']
        load_plan = req_json['plan']

        tdb = JmeterInfluxV1(influx_host=TDB_LT_HOST,
                             influx_port=TDB_LT_PORT,
                             influx_user=TDB_LT_USER,
                             influx_pwd=TDB_LT_PWD,
                             influx_db=TDB_LT_INST)
        data = tdb.export_metric(uid)

        lsm = LoadStepMetric(data, load_plan=load_plan, operation_column=['name'], time_column='time')
        lsm.metric('delay', rpm)
        lsm.metric('delay', avg)
        lsm.assemble_data_metric()

        insert_operations(session, [Operation(name[0]) for name in lsm.operation_name])
        report = insert_report(session, Report(report_name, lsm.start_time))
        add_report_operation(session, lsm, report.id)

        return jsonify(
            status='Ok',
            report_id=report.id
        )


@app.route("/load/profile", methods=['POST'])
def generate_profile():
    if request.method == 'POST':
        req_json = request.json
        start_date = req_json['start']
        end_date = req_json['end']

        tdb = JmeterInfluxV1(influx_host=TDB_PROD_HOST,
                             influx_port=TDB_PROD_PORT,
                             influx_user=TDB_PROD_USER,
                             influx_pwd=TDB_PROD_PWD,
                             influx_db=TDB_PROD_INST)

@app.route("/load/plan", methods=['POST'])
def add_plan():
    if request.method == 'POST':
        req_json = request.json

@app.route("/load/plan", methods=['GET'])
def get_plan():
    if request.method == 'POST':
        req_json = request.json
