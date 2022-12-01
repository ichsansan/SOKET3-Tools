import pandas as pd
import numpy as np
import os, re, time, config
from sqlalchemy import create_engine
from urllib.parse import quote

con = 'mysql+mysqlconnector://smlds:SMLds2021!@35.219.48.62/db_soket3'
box_link = 'https://box.ptpjb.com/s/eJBGmz4d3ykZso2'
old_excel_loc = '/mnt/disks/Others/Monitoring PJB Box/data/Excel Recap/'
old_box_loc = '/mnt/disks/Others/Monitoring PJB Box/data/5 Assesment Unit Pembangkit Terkait Implementasi/'
timezone = 7

def convert_size(number):
    suffix = ['','K','M','G','T','P']
    i = 0
    while number > 1500:
        number = number/1024
        i += 1
    return f"{round(number,2)} {suffix[i]}B"

def get_service_pjbboxcompare(data=None, datestart=None, dateend=None):
    data = {'daterange': '5DAY'}
    datestart = data['datestart'] if 'datestart' in data.keys() else None
    dateend = data['dateend'] if 'dateend' in data.keys() else None

    ret = {
        'columns': [],
        'content': []
    }

    engine = create_engine(con)
    project_name = 'PJB Box SOKET3'

    if (datestart is None) and (dateend is None):
        datestart, dateend = pd.to_datetime('now').floor('d'), pd.to_datetime('now') + pd.to_timedelta(f"{timezone}h")
    else:
        datestart = pd.to_datetime(datestart).strftime('%Y-%m-%d %X')
        dateend = pd.to_datetime(dateend).strftime('%Y-%m-%d %X')
    if pd.to_datetime(datestart) > pd.to_datetime(dateend):
        datestart, dateend = dateend, datestart
        
    if 'daterange' in data.keys():
        if data['daterange'] == 'TODAY':
            datestart = pd.to_datetime('now').floor('d')
            dateend = pd.to_datetime('now') + pd.to_timedelta(f"{timezone}h")
        else:
            datestart = pd.to_datetime('now').floor('d') - pd.to_timedelta(data['daterange'])
            dateend = pd.to_datetime('now') + pd.to_timedelta(f"{timezone}h")

    cols = config.project[project_name]['table_rename']
    cols = np.array(list(config.project[project_name]['table_rename'].values()))[np.argwhere([f is not None for f in cols.values()]).reshape(-1)].tolist()

    # TODO: Perbaiki variabel cols
    DI = pd.read_sql(f"""SELECT {','.join(cols)} FROM tb_daftar_isi_rekap 
                        WHERE f_project_name = "{project_name}" 
                        AND f_updated_at BETWEEN "{datestart}"
                        AND "{dateend}" """, engine)
    DI = DI.rename(columns=config.project[project_name]['table_rename'])
    DI.insert(0, 'Unit', [f.split('/')[0] for f in DI['File Location']])
    DI['File Location'] = [f"/{f[0].replace(f[1],'')}" for f in DI[['File Location','File Name']].values]
    DI['File Status'] = [f"<span class='badge bg-primary'>File baru</span>" if f == 1 else f"<span class='badge bg-danger'>File didelete</span>" for f in DI['File Status']]
    DI['Link'] = [f"""<a href='{box_link}?path={quote(f)}' target="_blank" rel="noopener noreferrer"><i class='fas fa-up-right-from-square'></i></a>""" for f in DI['File Location']]
    DI['File Size'] = [convert_size(int(f)) for f in DI['File Size']]
    DI = DI.drop(columns=['File Location'])
    
    ret['columns'] = list(DI.columns)
    ret['content'] = DI.to_dict(orient='records')
    return ret
    
def get_service_daftarisi(data = {}):
    ret = {
        'columns': [],
        'content': []
    }
    engine = create_engine(con)
    project_name = 'PJB Box SOKET3'
    if 'project_name' in data.keys(): project_name = data['project_name']

    Data = pd.read_sql( f"""SELECT f_filename, f_filesize, f_path, f_modified_time, f_updated_at FROM tb_daftar_isi_rekap WHERE f_project_name = "{project_name}" 
                            ORDER BY f_updated_at DESC, f_path ASC """, engine)
    Data = Data.groupby('f_path').first().reset_index()
    Data = Data.rename(columns={'f_filename': 'File Name', 'f_filesize':'File Size', 'f_path': 'File Path', 'f_modified_time':'Modified Time', 'f_updated_at':'Updated Time'})
    Data['Link'] = f"""<a href="{box_link}?path=""" + Data['File Path'] + "\">Link </a>"
    
    ret['columns'] = list(Data.columns)
    ret['content'] = Data.to_dict(orient='records')
    return ret

def get_service_perubahan_daftarisi(data = {}):
    ret = {
        'columns': [],
        'content': []
    }
    engine = create_engine(con)
    project_name = 'PJB Box SOKET3'
    datestart = pd.to_datetime('now').floor('d')
    dateend = pd.to_datetime('now') + pd.to_timedelta(f"{timezone}h")
    daterange = None
    total, limit, page = (0,0,0)
    if 'project_name' in data.keys(): project_name = data['project_name']
    if 'datestart' in data.keys(): datestart = pd.to_datetime(data['datestart'])
    if 'dateend' in data.keys(): dateend = pd.to_datetime(data['dateend'])
    if 'daterange' in data.keys(): daterange = data['daterange']
    if 'nlimit' in data.keys(): limit = data['nlimit']
    if 'npage' in data.keys(): page = data['npage']

    time.sleep(np.random.randint(10) / 1000)
    print(f"Get service perubahan daftar isi:", project_name, datestart, dateend, daterange)

    if daterange is not None:
        if daterange != 'Today':
            datestart = dateend - pd.to_timedelta(daterange)

    # Pagination
    l1 = 0; l2 = 100; LIMIT = ""
    if bool(page) or bool(limit):
        page = max([int(page),0]); limit = int(limit)
        l1 = (page) * limit
        l2 = (page+1) * limit
        LIMIT = f"LIMIT {l1},{l2}"

    cols = {k:v for k,v in config.project[project_name]['table_rename'].items() if v is not None}

    Data = pd.read_sql( f"""SELECT f_filename, f_filesize, f_path, f_modified_time, f_updated_at, f_file_status FROM tb_daftar_isi_rekap 
                            WHERE f_project_name = "{project_name}" AND f_updated_at BETWEEN "{datestart.strftime('%Y-%m-%d %X')}" AND "{dateend.strftime('%Y-%m-%d %X')}"
                            """, engine)
    Data = Data.groupby('f_path').first().reset_index()
    Data = Data.rename(columns={'f_filename': 'File Name', 'f_filesize':'File Size', 
                                'f_path': 'File Location', 'f_modified_time':'Modified Time', 
                                'f_updated_at':'Updated Time', 'f_file_status':'File Status'})

    Data.insert(0, 'Path', [f.split('/')[0] for f in Data['File Location']])
    Data['File Location'] = [f"/{f[0].replace(f[1],'')}" for f in Data[['File Location','File Name']].values]
    Data['File Status'] = [f"<span class='badge bg-primary'>File baru</span>" if f == 1 else f"<span class='badge bg-danger'>File didelete</span>" for f in Data['File Status']]
    if project_name == 'PJB Box SOKET3':
        Data['Link'] = [f"""<a href='{box_link}?path={quote(f)}' target="_blank" rel="noopener noreferrer"><i class='fas fa-up-right-from-square'></i></a>""" for f in Data['File Location']]
    Data['File Size'] = [convert_size(int(f)) for f in Data['File Size']]
    Data['Path'] = [f"""<span title="{l}" data-bs-placement="bottom">{p}/... </span> """ for p,l in Data[['Path','File Location']].values]
    
    Data = Data.drop(columns=['File Location','Modified Time'])

    # Paging
    total = len(Data)
    Data_page = Data.iloc[l1:l2]
    
    ret['datestart'] = datestart
    ret['dateend'] = dateend
    ret['columns'] = list(Data_page.columns)
    ret['content'] = Data_page.astype(str).to_dict(orient='records')
    ret['pagination'] = {
        'total': total,
        'page': page,
        'limit': limit
    }
    print(ret['pagination'])
    return ret

def get_service_recent_activity(data):
    ret = {}
    engine = create_engine(con)
    project_name = 'PJB Box SOKET3'
    
    if 'project_name' in data.keys(): project_name = data['project_name']
    q = f"""SELECT f_updated_at AS `date`, count(*) AS `filecount`, f_file_status AS file_status FROM tb_daftar_isi_rekap
            WHERE f_project_name = "{project_name}"
            GROUP BY f_updated_at, f_file_status 
            ORDER BY f_updated_at DESC """
    Data = pd.read_sql(q, con)
    Data['date'] = [f.strftime('%d %b') for f in Data['date']]
    Data['event'] = [f"Ada tambahan {e} file" if f==1 else f"Ada {e} file didelete" for e,f in Data[['filecount','file_status']].values]
    Data['color'] = [f"text-success" if f==1 else "text-danger" for f in Data['file_status'].values]
    Data = Data[['date','event','color']]
    ret = Data.astype(str).to_dict(orient='records')
    return ret

def get_service_taglists(unit):
    ret = {
        'columns': [],
        'content': []
    }
    unit = unit.replace('-', ' ')
    tb_im_tags = config.tables[unit]['tb_im_tags']

    Data = pd.read_sql( f"""SELECT f_tag_name AS TagName1, f_tag_name_alt1 AS TagName2, f_description AS Description 
                            FROM historian.{tb_im_tags} ORDER BY f_tag_name ASC """, con)
    ret = Data.astype(str).to_dict(orient='records')
    return ret

def get_service_tagrecap(unit):
    ret = {}
    unit = unit.replace('-', ' ')
    tb_im_tags = config.tables[unit]['tb_im_tags']
    tb_history = config.tables[unit]['tb_history']

    tagcount = pd.read_sql(f"""SELECT COUNT(*) FROM historian.{tb_im_tags}""", con).values[0][0]
    startdate, enddate = pd.read_sql(f"""SELECT min(f_date_rec), max(f_date_rec) FROM historian.{tb_history} """, con).values[0]
    ret = {
        'tagcount': str(tagcount),
        'startdate': pd.to_datetime(startdate).strftime('%Y-%m-%d %X'),
        'enddate': pd.to_datetime(enddate).strftime('%Y-%m-%d %X')
    }
    return ret

def get_service_daily_availability(unit):
    # TODO: Perbaiki ini
    ret = {}
    unit = unit.replace('-',' ')
    df = pd.read_csv('data/Data History Recap/Rekap persentase data SOKET3 - v2 - daily.csv', index_col='date')
    n = np.argwhere(df.columns.str.startswith(unit)).reshape(-1)
    if len(n) == 0: n = 0
    else: n = n[0]
    col = df.columns.values[n]

    ret = df[col].dropna().to_dict()
    return ret

def update_daftar_isi(project_name='PJB Box SOKET3'):
    PATH = '/content/drive/MyDrive/Working/SOKET 3.0 2022/'

    DI = []
    for r, fo, fi in os.walk(PATH):
        for file in fi:
            path = os.path.join(r, file)
            filepath = path.replace(PATH, '')
            filesize = os.path.getsize(path)
            filectime = pd.to_datetime(os.path.getctime(path) * 1e9)
            filemtime = pd.to_datetime(os.path.getmtime(path) * 1e9)
            DI.append([filepath, file, filesize, filectime, filemtime])

    DI = pd.DataFrame(DI, columns = ['File Location','File Name','File Size', 'Created Time', 'Modified Time'])

    cols = {
        'File Location': 'f_path',
        'File Name': 'f_filename',
        'Created Time': 'f_created_time',
        'Modified Time': 'f_modified_time',
        'File Size': 'f_filesize',
        'File Status': 'f_file_status'
    }
    DI_db = DI.rename(columns=cols)
    DI_db.insert(0, 'f_project_name', project_name)
    DI_db.insert(1, 'f_updated_at', pd.to_datetime('now') + pd.to_timedelta(f"{timezone}h"))
    print(f"Found {len(DI_db)} files on current files.")

    q = f"""SELECT f_updated_at,f_path,f_filename,f_created_time,f_modified_time FROM tb_daftar_isi_rekap
        WHERE f_project_name="{project_name}" ORDER BY f_updated_at DESC, f_path ASC """
    DI_latest = pd.read_sql(q, con)
    DI_latest = DI_latest.groupby('f_path').first().reset_index()
    print(f"Found {len(DI_latest)} files on the latest Table of Contents.")

    FileBaru = DI_db[[f not in DI_latest['f_path'].values for f in DI_db['f_path']]]
    FileDeleted = DI_latest[[f not in DI_db['f_path'].values for f in DI_latest['f_path']]]
    FileBaru['f_file_status'] = 1
    FileDeleted['f_file_status'] = 2

    DI_insert = FileBaru.append(FileDeleted, ignore_index=True)
    print(f"Inserting {len(DI_insert)} new recap ...")
    DI_insert.to_sql('tb_daftar_isi_rekap', con, if_exists='append', index=False)
    print('Insert success')
    
    ret = {
        'status': 'success',
        'message': f'Update successful with {len(DI_insert)} lines.'
    }
    return ret

def update_daftar_isi():
    PATH = old_box_loc
    project_name = "PJB Box SOKET3"

    DI = []
    for r, fo, fi in os.walk(PATH):
        for file in fi:
            path = os.path.join(r, file)
            filepath = path.replace(PATH, '')
            filesize = os.path.getsize(path)
            filectime = pd.to_datetime(os.path.getctime(path) * 1e9)
            filemtime = pd.to_datetime(os.path.getmtime(path) * 1e9)
            DI.append([filepath, file, filesize, filectime, filemtime])

    DI = pd.DataFrame(DI, columns = ['File Location','File Name','File Size', 'Created Time', 'Modified Time'])

    cols = {
        'File Location': 'f_path',
        'File Name': 'f_filename',
        'Created Time': 'f_created_time',
        'Modified Time': 'f_modified_time',
        'File Size': 'f_filesize',
        'File Status': 'f_file_status'
    }
    DI_db = DI.rename(columns=cols)
    DI_db.insert(0, 'f_project_name', project_name)
    DI_db.insert(1, 'f_updated_at', pd.to_datetime('now'))
    print(f"Found {len(DI_db)} files on current files.")

    q = f"""SELECT f_project_name,f_updated_at,f_path,f_filename,f_filesize,f_created_time,f_modified_time FROM tb_daftar_isi_rekap
        WHERE f_project_name="{project_name}" ORDER BY f_updated_at DESC, f_path ASC """
    DI_latest = pd.read_sql(q, con)
    DI_latest = DI_latest.groupby('f_path').first().reset_index()
    print(f"Found {len(DI_latest)} files on the latest Table of Contents.")

    FileBaru = DI_db[[f not in DI_latest['f_path'].values for f in DI_db['f_path']]]
    FileDeleted = DI_latest[[f not in DI_db['f_path'].values for f in DI_latest['f_path']]]
    FileBaru['f_file_status'] = 1
    FileDeleted['f_file_status'] = 2

    DI_insert = FileBaru.append(FileDeleted, ignore_index=True)
    DI_insert["f_updated_at"] = pd.to_datetime("now") + pd.to_timedelta("7h")
    print(f"Inserting {len(DI_insert)} new recap ...")
    if len(DI_insert)>0: 
        DI_insert.to_sql('tb_daftar_isi_rekap', con, if_exists='append', index=False,)
        return 'Insert success'
    return 'No data to insert'

# Old Services
def services_old_home(data):
    ret = {
        'filename': '',
        'filelist': {
            'filename':[],
            'filedate':[]
        },
        'filedate':{
            'current':'',
            'previous':'',
        },
        'contents':{
            'columns': [],
            'data': []
        }
    }

    files = np.sort([f for f in os.listdir(old_excel_loc) if f.endswith('.xlsx')]).tolist()
    Files = pd.DataFrame()
    Files['Nama File'] = files

    # Check latest data
    tanggalfiles = [pd.to_datetime(f.split(' - ')[-1].split('.')[0]) for f in files]
    Files['Tanggal File'] = tanggalfiles
    Files = Files.sort_values('Tanggal File', ascending=False)
    ret['filename'] = Files.iloc[0]['Nama File']
    ret['filedate']['current'] = Files.iloc[0]['Tanggal File'].strftime('%Y-%m-%d %X')
    ret['filedate']['previous'] = Files.iloc[1]['Tanggal File'].strftime('%Y-%m-%d %X')
    ret['filelist']['filename'] = files
    ret['filelist']['filedate'] = [f.strftime('%Y-%m-%d %X') for f in tanggalfiles]

    CurrentFile = Files.iloc[0]['Nama File']
    PreviousFile = Files.iloc[1]['Nama File']
    if 'currentfile' in data.keys(): 
        CurrentFile = data['currentfile']
        ret['filedate']['current'] = pd.to_datetime(CurrentFile.split(' - ')[-1].split('.')[0]).strftime('%Y-%m-%d %X')
    if 'previousfile' in data.keys(): 
        PreviousFile = data['previousfile']
        ret['filedate']['previous'] = pd.to_datetime(PreviousFile.split(' - ')[-1].split('.')[0]).strftime('%Y-%m-%d %X')
    if pd.to_datetime(ret['filedate']['current']) < pd.to_datetime(ret['filedate']['previous']):
        CurrentFile, PreviousFile = PreviousFile, CurrentFile
        ret['filedate']['current'] = pd.to_datetime(CurrentFile.split(' - ')[-1].split('.')[0]).strftime('%Y-%m-%d %X')
        ret['filedate']['previous'] = pd.to_datetime(PreviousFile.split(' - ')[-1].split('.')[0]).strftime('%Y-%m-%d %X')

    File1 = pd.read_excel(os.path.join(old_excel_loc, CurrentFile))
    File1 = File1.drop(columns=File1.columns[0])
    File2 = pd.read_excel(os.path.join(old_excel_loc, PreviousFile))
    File2 = File2.drop(columns=File2.columns[0])

    Rekaps = File1.append(File2, ignore_index=True).drop_duplicates().reset_index(drop=True)
    Rekaps['File Baru'] = [f not in (File2['Path'].values) for f in Rekaps['Path']]
    Rekaps['File Lama Didelete'] = [f not in (File1['Path'].values) for f in Rekaps['Path']]
    Rekaps = Rekaps[Rekaps[['File Baru','File Lama Didelete']].max(axis=1)]
    Rekaps['Status'] = ['File baru' if f else 'Di delete' for f in Rekaps['File Baru']]
    Rekaps = Rekaps.drop(columns=['File Baru','File Lama Didelete','File Size (bytes)'])

    ret['contents']['columns'] = Rekaps.columns.to_list()
    ret['contents']['data'] = Rekaps.to_dict(orient='records')
    return ret

def services_old_update():
    path = old_box_loc
    DaftarIsi = []

    for r, fo, fi in os.walk(path):
        for file in fi:
            filepath = os.path.join(r, file)
            filedir = filepath.replace(path,'')
            fileext = file.split('.')[-1]
            filemtime = pd.to_datetime(os.path.getmtime(filepath) * 1e9) + pd.to_timedelta('7h')
            filesize = os.path.getsize(filepath)
            filersize = convert_size(filesize)
            DaftarIsi.append([filedir, file, fileext, filemtime, filesize, filersize])
    DaftarIsi = pd.DataFrame(DaftarIsi, columns = ['Path','File Name', 'Extension','Last Modified','File Size (bytes)','Readable File Size'])
    now = pd.to_datetime('now') + pd.to_timedelta('7h')
    filename = f"Daftar Isi PJB Box SOKET3 - {now.strftime('%Y%m%d %H%M%S')}.xlsx"
    DaftarIsi.to_excel(os.path.join(old_excel_loc, filename))

    return f'File saved to {filename}'
