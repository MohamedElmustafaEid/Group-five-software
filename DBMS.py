
from psycopg2 import connect
import json
import requests
import geopandas as gpd
import pandas as pd
import fiona
from sqlalchemy import create_engine


cleanup = (
        'DROP TABLE IF EXISTS sys_table CASCADE',
        'DROP TABLE IF EXISTS comment_table',
        'DROP TABLE IF EXISTS data_table'
        )

commands =(
        """
        CREATE TABLE sys_table (
            userid SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            age INTEGER
        )
        """
        ,
        """
        CREATE TABLE comment_table (
            comment_id SERIAL PRIMARY KEY,
            userid INTEGER NOT NULL UNIQUE,
            created TIMESTAMP DEFAULT NOW(),
            comment VARCHAR(500) NOT NULL,
            FOREIGN KEY (userid)
                    REFERENCES sys_table (userid)
 
        )
        """
        ,
        """
        CREATE TABLE data_table (
            patient_id INTEGER NOT NULL UNIQUE,
            long POINT NOT NULL,
            lat POINT NOT NULl,
            interview_date DATE ,
            gender VARCHAR(255),
            marital_status VARCHAR(255),
            religion VARCHAR(255),
            patient_education_level VARCHAR(255),
            ethinc_group VARCHAR(255),
            disease_stegma VARCHAR(255),
            time_from_first_sym DATE,
            first_doctor_visit DATE
        )
        """)

sqlInsert= """ INSERT INTO sys_table (username, password, email, age) VALUES(%s,%s,%s,%s) RETURNING userid; """
sqlQuery= """ SELECT * FROM sys_table; """
conn = connect("dbname=postgres user=postgres host=localhost password=1234")
cur = conn.cursor()

for command in cleanup:
    cur.execute(command)
for command in commands:
    cur.execute(command)


cur.execute(sqlInsert, ('Gio', '123', 'mustafa881995@gmail.com', '25'))
userId = cur.fetchone()[0]
cur.execute(sqlQuery)

cur.close()
conn.commit()
conn.close()

response = requests.get('https://five.epicollect.net/api/export/entries/ug-hatua-phase-2-adult-outpatients?per_page=739')
rawdata = response.text
data   = json.loads(rawdata)
data_df = pd.json_normalize(data['data']['entries'])

data_df['Patient_id'] = data_df['3_Patient_ID']
data_df['long'] = pd.to_numeric(data_df['8_Location.longitude'], errors='coerce')
data_df['lat'] = pd.to_numeric(data_df['8_Location.latitude'], errors='coerce')
data_df['Interview_data'] = data_df['6_Interview_Date']
data_df['Gender'] = data_df['20_Gender_interviewe']
data_df['Marital_Status'] = data_df['22_What_is_your_mari']
data_df['Religion'] = data_df['26_Religion_can_infl']
data_df['Education_level'] = data_df['23_What_is_the_highe']
data_df['time_from_first_symptom'] = data_df['56_When_did_you_firs']
data_df['disease_stigma'] = data_df['57_Do_these_symptoms']
data_df = data_df.loc[:,'Patient_id':'disease_stigma']

engine = create_engine('postgresql://postgres:1234@localhost:5432/postgres')
data_df.to_sql('data_table', engine, if_exists = 'replace', index=False)