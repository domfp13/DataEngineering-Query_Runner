# DataEngineering-Query_Runner
This is the Query_Runner project, this project takes a SQL query and runs it against our Oracle DW, the data that is produced it is later on sent to an AWS s3 bucket.

## Getting Started

### 1- Prerequisites
* [Anaconda]() - Anaconda allows us to keep virtual environments organize and it is the best setup tool for data analysis. This code needs python 3.7

### 2- Installing requirementes
```sh
$ git clone ~/DataEngineering-Query_Runner.git
$ conda create -n Query_Runner python=3.7
$ conda activate Query_Runner
$ cd DataEngineering-Query_Runner
$ pip install requirements.txt
```
### 3- Description
This project requires a query that has to be placed inside of the etl directory and it also has to be part of the REGISTRY dictionary, once the query is placed as a function in the etl/queries.py and it is added to the REGISTRY this project could run as:
```sh
$ python main.py "query_name"
```
Note: If the query contains biding parameters they code needs to be fixed.
## Authors
* **Enrique Plata** - *2020/01/27*