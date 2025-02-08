CREATE OR REPLACE TABLE dez2025.wk3.yellow_materialized AS
SELECT * FROM dez2025.wk3.yellow;

-- Question 1
SELECT count(*) FROM `dez2025.wk3.yellow` ;

-- Question 2
select count(distinct(PULocationID))
FROM `dez2025.wk3.yellow`;

-- Question 3
select PULocationID
FROM `dez2025.wk3.yellow`;

select PULocationID,DOLocationID
FROM `dez2025.wk3.yellow`;

-- Question 4
SELECT count(*) FROM `dez2025.wk3.yellow` 
where fare_amount=0;

-- Question 5
CREATE OR REPLACE TABLE dez2025.wk3.opt_yellow
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM dez2025.wk3.yellow;

-- Question 6
select distinct(PULocationID)
from dez2025.wk3.yellow_materialized
where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15';

select distinct(PULocationID)
from dez2025.wk3.opt_yellow
where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15';



