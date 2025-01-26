# Queries Used

3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
```
select count(*) 
from taxi_data.yellow_tripdata
where SPLIT(SPLIT(filename, '_')[OFFSET(2)],'-')[OFFSET(0)] ='2020';
```
4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?
```
select count(*) 
from taxi_data.green_tripdata
where SPLIT(SPLIT(filename, '_')[OFFSET(2)],'-')[OFFSET(0)] ='2020';

```
5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
```
select count(*) 
from taxi_data.yellow_tripdata
where SPLIT(SPLIT(filename, '_')[OFFSET(2)],'-')[OFFSET(0)] ='2021' 
and SPLIT(SPLIT(SPLIT(filename, '_')[OFFSET(2)],'-')[OFFSET(1)],'.')[OFFSET(0)] ='03';
```