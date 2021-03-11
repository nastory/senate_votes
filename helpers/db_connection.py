# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:20:09 2019

@author: nigels
"""

try:
    import mysql.connector as sql
    from sqlalchemy import create_engine
    import pandas as pd
except ImportError as error:
    print(error.__class__.__name__ + ":" + error.message)

class DBConnect():
    """
    Class for connecting to and executing cammands on 
    locally hosted MySQL db.
    """
    
    def __init__(self, db, autocommit=False):
        self.db_name = db.lower()

        self.engine = create_engine(
         f'mysql+mysqlconnector://root:@localhost:3306/{db}',
         echo=False, connect_args={'connect_timeout': 300})

        self.cnx = sql.connect(
                host='localhost',
                user='root',
                passwd='',
                database=self.db_name       
                )
        
        self.cur = self.cnx.cursor()
        self.cnx.autocommit = autocommit
        
    def __enter__(self, autocommit=False):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
    
    def close(self):
        self.cur.close()
        self.cnx.close()
    
    def execute_from_file(self, file_path):

        with open(file_path, 'r') as f:
            sql_file = f.read()

        commands = sql_file.split(';') 

        for command in commands:
            try:
                if command.strip() != '':
                    self.cur.execute(command)
            except(IOError) as msg:
                print("Command skipped: ", msg)

    def df2db(self, df, table_name, method='replace', if_dup_key_replace=False):
    
        method = method.upper()
        table_name = table_name.upper()
        
        if method not in ['REPLACE', 'INSERT']:
            raise ValueError('Method must be one of "replace" or "insert".')
        
        query = "{} INTO {}.{} ({}) VALUES ({})"
        colstr = ', '.join(df.columns)
        paramstr = ', '.join(['%s' for s in df.columns])
        
        query = query.format(method, self.db_name, table_name, colstr, paramstr)
        
        if (method == 'INSERT') and if_dup_key_replace:
            update_cols = ' ,'.join(['{} = VALUES({})'.format(x,x) for x in df.columns])
            on_dup = " ON DUPLICATE KEY UPDATE {};".format(update_cols)
            query += on_dup
        
        df.fillna('NULL', inplace=True)
        tups = [tuple(x) for x in df.to_numpy()]
        
        start = 0
        while start <= len(tups):
            end = start + 1000
            chunk = tups[start: end]
            self.cur.executemany(query, chunk)
            start = end
        
        self.cnx.commit()
