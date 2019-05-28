import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect

import pandas as pd
import datetime
import time

import os
import psycopg2

from wrangling_scripts.twitch_api_funcs import get_top_games


def get_sql_engine(DATABASE_URL=None):
    '''
    INPUTS:
        DATABASE_URL (string): database url. should be given from the main dyno env
    RETURNS:
        engine (sqlalchemy engine): 
    '''
        
    # get environment var if possible
    if DATABASE_URL is None:
        DATABASE_URL = os.environ['DATABASE_URL']

    engine = create_engine(DATABASE_URL)
    
    return engine
    
def recreate_table(database_url, table_name):
    create_command = 'CREATE TABLE {} ( time VARCHAR(255) NOT NULL, \
                                           game VARCHAR(255) NOT NULL, \
                                           viewers INTEGER NOT NULL, \
                                           streams INTEGER NOT NULL )'.format(table_name)
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    try:
        cur.execute(create_command)
    except Exception as e:
        print(e)
    
    conn.commit()
    cur.close()
    conn.close()
    return
    
    
def check_table_size(engine, table_name):
    '''
    INPUTS:
        engine: sqlalchemy engine
        table_name (string): name of table to interact with
    RETURNS:
        num_rows (int): number of rows found in table
    '''
    
    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(*) FROM {};'.format(table_name))
        num_rows = cur.fetchall()[0][0]
        print('found {} rows in database'.format(num))
    except Exception as e:
        print(e)
        conn.rollback()
        
    cur.close()
    conn.close()
    
    return num_rows
    
    
def append_to_table(engine, table_name):
    '''
    INPUTS:
        engine: sqlalchemy engine
        table_name (string): name of table to interact with
    RETURNS: none
    '''
    
    df = get_top_games()
    df.to_sql(table_name, engine, index=False, if_exists='append')
    
    return


def del_from_table(engine, table_name): # CURRENTLY ONLY WORKS WITH A TABLE WITH A TIME COLUMN
    '''
    INPUTS:
        engine: sqlalchemy engine
        table_name (string): name of table to interact with
    RETURNS: none
    '''
    
    # get oldest entry datetime
    df = pd.read_sql_table(table_name, con = engine)
    df['time'] = pd.to_datetime(df['time'])
    mintime = df['time'].min().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(mintime)
    
    # get raw postsql connection and cursor from engine
    conn = engine.raw_connection()
    cur = conn.cursor()
    # delete 
    cur.execute("DELETE FROM games_table WHERE time = %s", (mintime,))
    conn.commit()
    cur.close()
    conn.close()
    
    
def extract_all_from_table(engine, table_name): # CURRENTLY ONLY WORKS WITH A TABLE WITH A VIEWER AND TIME COLUMN
    '''
    INPUTS:
        engine: sqlalchemy engine
        table_name (string): name of table to interact with
    RETURNS:
        df (DataFrame): dataframe containing all data from the table
    '''
    df = pd.read_sql_table(table_name, con = engine)
    df['time'] = pd.to_datetime(df['time'])
    df['viewers'] = pd.to_numeric(df['viewers'])
    
    return df


def scheduled_sql_task(engine, table_name, max_size=9000):
    '''
    This function will try to create the table if it does not exist already.
    Then it will call a function to add query the twitch API and add new rows to the table.
    Then, it will check how many rows exist in the table.
    If the number of rows exceeds the max_size var, it will delete rows until the number of rows is < max_size
    INPUTS:
        engine: SQLalchemy engine created from the database URL (local var on main dyno)
        table_name (string): the name of the table to interact with
        max_size (int): the size at which the function will remove rows to make room for new ones
    RETURNS: None
    '''
    
    # add data
    append_to_table(engine, table_name)
    print('added rows')
    
    # check size
    num_rows = check_table_size(engine, table_name)
    print('table has {} rows'.format(num_rows))
    while num_rows > max_size:
        print('deleting rows...')
        del_from_table(engine, table_name)
        num_rows = check_table_size(engine, table_name)
    
    
