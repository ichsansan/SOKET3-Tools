from flask import Flask, render_template, jsonify, request, flash, send_file
from servicehandler import *
import pandas as pd
import numpy as np
import os, time, re, requests

app = Flask(__name__)
app.secret_key = "e236c78afcb9a393ec15f71bbf5dc987d547278"

@app.route('/')
def home():
    data = {}
    return render_template('Homepage.html', data = data)

@app.route('/DriveMonitoring/PJBBox')
def pjbbox():
    return render_template('DriveMonitoring-PJBBox.html')

@app.route('/DriveMonitoring/GdriveSML')
def gdrivesml():
    return render_template('DriveMonitoring-GdriveSML.html')

@app.route('/HistorianRecap/<unit>')
def HistorianRecap(unit):
    return render_template('HistorianRecap.html', unit=unit, title=f"Historian Recap - {unit}")

################### API ###################
@app.route('/services/daftar-isi/compare')
def service_pjbbox_compare():
    ret = {
        'status': 'failed',
        'message': '',
    }
    data = {}
    for k in ['project_name','datestart','dateend','daterange']:
        val = request.args.get(k, default=None, type=str)
        if val: data[k] = val
    
    try:
        ret['content'] = get_service_perubahan_daftarisi(data)
        ret['status'] = 'success'
    except Exception as E:
        ret['message'] = str(E)
    return jsonify(ret)

@app.route('/services/daftar-isi/daftar-isi')
def service_pjbbox_daftarisi():
    ret = {
        'status': 'failed',
        'message': '',
    }
    data = dict(request.get_data())
    try:
        ret['content'] = get_service_daftarisi(data)
        ret['status'] = 'success'
    except Exception as E:
        ret['message'] = str(E)
    return jsonify(ret)

@app.route('/services/historian-recap/<unit>')
def service_historian_taglist(unit):
    ret = {
        'status': 'failed',
        'message': '',
    }
    try:
        ret['content'] = get_service_taglists(unit)
        ret['status'] = 'success'
    except Exception as E:
        ret['message'] = str(E)
    return jsonify(ret)

@app.route('/services/historian-tag-recap/<unit>')
def service_historian_tagrecap(unit):
    ret = {
        'status': 'failed',
        'message': '',
    }
    try:
        ret['content'] = get_service_tagrecap(unit)
        ret['status'] = 'success'
    except Exception as E:
        ret['message'] = str(E)
    return jsonify(ret)

@app.route('/services/historian-daily-availability/<unit>')
def service_historian_daily_availability(unit):
    ret = {
        'status': 'failed',
        'message': '',
    }
    try:
        ret['content'] = get_service_daily_availability(unit)
        ret['status'] = 'success'
    except Exception as E:
        ret['message'] = str(E)
    return jsonify(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)