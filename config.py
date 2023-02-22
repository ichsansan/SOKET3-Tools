tables = {
    'PLTU Bangka': {
        'tb_history': 'tb_history_bangka',
        'tb_im_tags': 'tb_im_tags_bangka',
        'timestep': '5min',
    },
    'PLTU Kendari': {
        'tb_history': 'tb_history_kendari',
        'tb_im_tags': 'tb_im_tags_kendari',
        'timestep': '5min',
    },
    'PLTU Pulang Pisau': {
        'tb_history': 'tb_history_pulang_pisau',
        'tb_im_tags': 'tb_im_tags_pulang_pisau',
        'timestep': '5min',
    },
    'PLTU Tidore': {
        'tb_history': 'tb_history_tidore',
        'tb_im_tags': 'tb_im_tags_tidore',
        'timestep': '5min',
    },
    'PLTU Paiton 9': {
        'tb_history': 'tb_history_paiton9',
        'tb_im_tags': 'tb_im_tags_paiton9',
        'timestep': '5min',
    },
}

cols = ['f_project_name', 'f_updated_at', 'f_path', 'f_filename','f_created_time', 'f_modified_time', 'f_filesize','f_file_status']

project = {
    'PJB Box SOKET3':{
        'link': 'https://box.ptpjb.com/s/eJBGmz4d3ykZso2?path={{dir}}',
        'table_rename':{
            'f_id': None,
            'f_project_name':None,
            'f_path': None,
            'f_filename': 'File Name',
            'f_created_time': None,
            'f_modified_time': 'Modified Time',
            'f_filesize': 'File Size',
            'f_file_status': 'File Status'
        }
    },
    'Google Drive SOKET3':{
        'link': 'https://drive.google.com/drive/folders/1gBXEJ6Wyc0e8iI6M-phEXNtjQlAixxVQ',
        'table_rename':{
            'f_id': None,
            'f_project_name':None,
            'f_path': 'File Location',
            'f_filename': 'File Name',
            'f_created_time': None,
            'f_modified_time': 'Modified Time',
            'f_filesize': 'File Size',
            'f_file_status': 'File Status'
        }
    },
    'PLNNP Google Drive':{
        'link': 'https://drive.google.com/drive/folders/1ltcYtfNijJCqXYvRwRoXrOhgLzdXtzcB',
        'table_rename':{
            'f_id': None,
            'f_project_name':None,
            'f_path': 'File Location',
            'f_filename': 'File Name',
            'f_created_time': None,
            'f_modified_time': 'Modified Time',
            'f_filesize': 'File Size',
            'f_file_status': 'File Status'
        }
    }
}