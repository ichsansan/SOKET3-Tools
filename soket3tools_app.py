from flask import Flask, render_template, jsonify, request, flash, send_file
from servicehandler import *
import pandas as pd
import numpy as np
import os, time, re, requests, sys

app = Flask(__name__)
app.secret_key = "e236c78afcb9a393ec15f71bbf5dc987d547278"

@app.route('/')
def home():
    data = {}
    return render_template('Homepage.html', data = data)

@app.route('/DriveMonitoring/<project_name>')
def pjbbox(project_name):
    project_name = project_name.replace('-',' ')
    return render_template('DriveMonitoring.html', project_name=project_name)

@app.route('/HistorianRecap/<unit>')
def HistorianRecap(unit):
    return render_template('HistorianRecap.html', unit=unit, title=f"Historian Recap - {unit}")

################### OLD ###################
@app.route('/old')
def old_home():
    try:
        data = dict(request.values)
        print('Data request: ', data)
        ret = old_home(data)

    except Exception as E:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        flash(f"Error: {E}")
    return render_template('old-home.html', data = ret)

@app.route('/old-file')
def old_file():
    data = dict(request.values)
    files = np.sort(os.listdir(old_excel_loc)).tolist()
    
    # Check latest data
    filesdate = [pd.to_datetime(f.split(' - ')[-1].split('.')[0]) for f in files]
    file = files[np.argmax(filesdate)]

    if 'file' in data.keys():
        if os.path.isfile(os.path.join(old_excel_loc,data['file'])): 
            file = data['file']
        else:
            flash(f"File: `{file}` not found!")

    return render_template('old-file.html', file=file, listfiles=files)

# API
@app.route('/old-getfile/<filename>')
def get_file(filename: str):
    Data = pd.read_excel(os.path.join(old_excel_loc, filename))
    Data = Data.set_index(Data.columns[0])
    Data['Last Modified'] = [f.strftime('%Y-%m-%d %H:%M:%S') for f in Data['Last Modified']]
    return jsonify(Data.to_dict('records'))

@app.route('/old-download/<filename>')
def download(filename: str):
    filename = os.path.join(old_excel_loc, filename)
    return send_file(filename, as_attachment=True)

@app.route('/old-update')
def update():
    ret = {
        'status':'Failed',
        'message':''
    }

    try:
        ret['message'] = old_update()
        ret['status'] = 'Success'
    except Exception as E:
        ret['message'] = str(E)
    return jsonify(ret)

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

@app.route('/service/daftar-isi/recent-activity')
def service_recent_activity():
    ret = {
        'status': 'failed',
        'message': '',
    }
    
    data = {}
    for k in ['project_name']:
        val = request.args.get(k, default=None, type=str)
        if val: data[k] = val
    print(data)

    try:
        ret['content'] = get_service_recent_activity(data)
        ret['status'] = 'success'
    except Exception as E:
        ret['message'] = str(E)
    
    return jsonify(ret)

@app.route('/services/daftar-isi/update')
def service_daftar_isi_update():
    ret = {
        'status': 'failed',
        'message': '',
    }
    try:
        ret['message'] = update_daftar_isi()
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