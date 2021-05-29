# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 13:15:51 2021

@author: aa.221599
"""


import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os
import mysql.connector
import re
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIA4HGHG44HSWHZGMQV'
SECRET_KEY = '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'

def conn():
    host='rds-mysql-database-dspd-1.cwnbtme3ltl9.us-east-1.rds.amazonaws.com'
    port=int(3306)
    user='DSPD'
    passw='dspd1234'
    database='dspd_ml'

    mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + 
                     ':' + str(port) + '/' + database , echo=False)
    return mydb
    

def file_to_mysql(corpus,mydb):
    
    db=mydb
    path=os.path.abspath(os.getcwd())+'\\DataScience-Projects-master\\'
    print(path)
    train_data = pd.read_csv(path + 'train.csv')
    train_data.to_sql(name='training_data', con=db, if_exists = 'append', index=False)
    test_data = pd.read_csv(path + 'test.csv')
    test_data.to_sql(name='test_data', con=db, if_exists = 'append', index=False)

def file_to_mysql_full(conn):
    
   
    path=os.path.abspath(os.getcwd())+'\\training_Data\\'

    train_data = pd.read_csv(path + 'training_full_data-part5.csv')
    train_data.to_sql(name='training_full_data', con=conn, if_exists = 'append', index=False)
    # df.to_sql(name='training_full_data', con=conn, if_exists = 'append', index=False)
    
def file_processing(file):
    path=os.path.abspath(os.getcwd())+'\\training_Data\\'
    train = pd.read_csv(path + 'training_full_data-part1.csv', usecols=[1,2,3,4,5,6],names=['sentiment', 'textID','date','no_query','special','text'],encoding='latin-1')
    df = pd.DataFrame(train)
    # row_indexes=df[df['sentiment']==0].index
    # df.loc[row_indexes,'sentiment']="negative"
    # row_indexes=df[df['sentiment']==2].index
    # df.loc[row_indexes,'sentiment']="neutral"
    # row_indexes=df[df['sentiment']==4].index
    # df.loc[row_indexes,'sentiment']="positive"
    df['text']=df['text'].apply(lambda x: re.sub(r'@[\w]+', '', x))
    df.to_csv(path+'training_full_data_new.csv')
    return df
    #print(df['sentiment'],df['textID'])

def training_data_update(mydb):
    

    mydb = mysql.connector.connect(
        host="rds-mysql-database-dspd-1.cwnbtme3ltl9.us-east-1.rds.amazonaws.com", 
        user="DSPD",
        password="dspd1234",
        database="dspd_ml"
        )

    mycursor = mydb.cursor()
    sql = " REPLACE INTO dspd_ml.training_data  select textID,text,text, case when sentiment = 0 then 'negative' when sentiment = 2 then 'neutral' when sentiment = 4 then 'positive' end as setiment from dspd_ml.training_full_data order by rand() limit 500"
    mycursor.execute(sql)
    mydb.commit()

def push_to_s3(conn,ACCESS_KEY,SECRET_KEY):
    dbConnection = conn.connect()
    frame = pd.read_sql("select * from dspd_ml.training_data", dbConnection);
    path=os.path.abspath(os.getcwd())+'\\DataScience-Projects-master\\training_Data\\Actual_chunk_data\\'
    frame.to_csv(path+'train_data.csv',index = False)
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    path_s3=path +'train_data.csv'

    try:
        s3.upload_file(path_s3, 'dspd-data-science', 'train_data.csv')
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

    



    
# df = file_processing("")
#file_to_mysql("",conn())
#file_to_mysql_full(conn())
#training_data_update("")  
push_to_s3(conn(),ACCESS_KEY,SECRET_KEY) 
