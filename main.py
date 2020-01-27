# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes
# To run: python main.py open_case_tracking_numbers

from __future__ import annotations
from typing import Optional
from pathlib import Path
from etl.queries import (open_case_tracking_numbers)
from etl.db_connection import OracleConnection
from etl.extract import (to_csv, to_bucket, delete_processed_file)
import datetime
import logging
import sys
import os

REGISTRY = {
    'open_case_tracking_numbers': [1, open_case_tracking_numbers()]
}

if __name__ == "__main__":
    """ 
    Executes and retrieves a dataset from DW-SQL Server, after retrieving data it posted the file in a CSV format in a bucket in AW.
  
    Parameters: 
    arg1 (int): Description of arg1 
  
    Returns: 
    int: Description of return value 
  
    """
    try:
        # 0.- Setup the logging object
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        loggin_file_path = str(Path('{path}/Query_Runner.log'.format(path = os.getcwd())))
        logging.basicConfig(filename = loggin_file_path,
                            level = logging.DEBUG,
                            format = LOG_FORMAT,
                            filemode = 'w')
        
        logger = logging.getLogger()

        # There is one parameter by defaul 
        if len(sys.argv) == 2 and str(sys.argv[1]) in REGISTRY:
            
            # 1- Getting arguments
            query_to_execute = str(sys.argv[1])

            # 2.- Connecting to DW
            logger.info("Stablishing connection with DW")
            oracle_conn = OracleConnection()

            # 3.- Running query and creating CSV
            if len(REGISTRY[query_to_execute]) == 2:
                logger.info(f"Running query {str(sys.argv[1])}")
                col_names, data = oracle_conn.sql_to_data_no_binding(REGISTRY[query_to_execute][1])
            else:
                logger.info(f"Running query {str(sys.argv[1])}")
                data = oracle_conn.sql_to_data(REGISTRY[query_to_execute][1], REGISTRY[query_to_execute][2])
            
            fileNameOutput = f'{str(sys.argv[1])}_{str(datetime.date.today())}.csv'

            # 4.- Writting Data to CSV file
            logger.info("Writting data to CSV")
            to_csv(fileNameOutput, data, col_names)
            logger.info("Done running query and creating CSV")

            # 5.- Send file to bucket
            logger.info("Uploading file to bucket")
            to_bucket(fileNameOutput)
            logger.info("File uploaded")

            # 6.- Remove file
            logger.info("Deleting local file")
            delete_processed_file(f'{os.getcwd()}/{fileNameOutput}')
            logger.info("File deleted")

        else:
            logger.info(f"Query {str(sys.argv[1])} Not in REGISTRY") 
            logger.info("Parameter not specified")

    except Exception as e:
        logger.error(e)
        sys.exit()