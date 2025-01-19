#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import math
import pandas as pd
from sqlalchemy import create_engine,text

def load_data(engine, table_name, file_name):
    print(f'Loading {file_name} into {table_name}')
    df = pd.read_csv(f'datasets/{file_name}',low_memory=False)
    try:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    except Exception as e:
        pass
   
    df.head(n=0).to_sql(name=f'{table_name}', con=engine, if_exists='replace')

    n = 100000
    batches = math.ceil(len(df)/n)
    for i in range(0,len(df),n):
        batch = 1 if i == 0 else int((i/n)+1)
        print(f'inserting batch {batch} of {batches}...')
        df[i:i+n].to_sql(name=f'{table_name}', con=engine, if_exists='append')


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    
    configuration = {'green_tripdata':'green_tripdata_2019-10.csv',
                     'taxi_zone_lookup':'taxi_zone_lookup.csv'}
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if params.load_data is True:
        for table_name, file_name in configuration.items():
            load_data(engine=engine,table_name=table_name,file_name=file_name)
    else:
        print('Skipping data loading')
    
    
    questions_3=[
                '''select count(*) from green_tripdata 
                    where trip_distance<=1.0;''',
                '''select count(*) from green_tripdata 
                    where trip_distance>1.0 and trip_distance<=3.0;''',
                '''select count(*) from green_tripdata 
                    where trip_distance>3.0 and trip_distance<=7.0;''',
                '''select count(*) from green_tripdata 
                    where trip_distance>7.0 and trip_distance<=10.0;''',
                '''select count(*) from green_tripdata 
                    where trip_distance>10.0;''',
                ]
    questions_4='''select lpep_pickup_datetime::date,max(trip_distance) as max_dist
                   from green_tripdata
                   group by lpep_pickup_datetime::date
                   order by max_dist desc
                   limit 1;'''
    question_5='''with rows as(
                  select "PULocationID" as location_id,sum(total_amount) total_amount_sum
                  from green_tripdata
                  where lpep_pickup_datetime::date = '2019-10-18'
                  group by "PULocationID"
                  order by total_amount_sum desc
                  limit 3)
                  select (select "Zone" from taxi_zone_lookup where "LocationID"=location_id)
                  from rows;'''
    question_6='''select (select "Zone" from taxi_zone_lookup where "LocationID"="DOLocationID"), 
                  max(tip_amount) max_tip
                  from green_tripdata
                  where "PULocationID" = (
                  select "LocationID" from taxi_zone_lookup
                  where "Zone"='East Harlem North') and EXTRACT('MONTH' FROM lpep_pickup_datetime)=10
                  group by "DOLocationID"
                  order by max_tip desc
                  limit 1'''
                 
    answer3=[]
    with engine.connect() as conn:
        for question in questions_3:
            res = conn.execute(text(question))
            answer3.append(f'{res.all()[0][0]:,}')
        answer4 = conn.execute(text(questions_4)).all()[0][0]
        answer5 = [zone[0] for zone in conn.execute(text(question_5)).all()]
        answer6 = conn.execute(text(question_6)).all()[0][0]
        
        
    print('Answer 3:', '; '.join(answer3))
    print('Answer 4:', answer4)
    print('Answer 5:', ', '.join(answer5))
    print('Answer 6:', answer6)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest Parquet data to PSQL')
    parser.add_argument('--user', help='user name for psql')
    parser.add_argument('--password', help='password for psql')
    parser.add_argument('--host', help='host for psql')
    parser.add_argument('--port', help='port for psql')
    parser.add_argument('--db', help='database name for psql')
    parser.add_argument('--load_data', default=True, help='define if we want to reload data. Default is True')


    args = parser.parse_args()

    main(args)


