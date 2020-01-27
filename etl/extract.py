# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes

def to_bucket(fileName:str)->None:
    """This funtion uploads a file to an S3 bucket

    Arguments
     file (str): String containing the name of the file that will be loaded
    
    Returns
     None
    """
    import boto3
    import os
    from pathlib import Path

    s3_client = boto3.client('s3')

    bucket = "data-engineering-preprod"
    # bucket = "domfp13-s3-bucket"

    dictionary = {'bucketName': bucket, 
            'destination_blob_name': f'dw_data/{fileName}',
            'source_file_name': f'{os.getcwd()}/{fileName}'}

    path = Path(dictionary['source_file_name'])

    with path.open("rb") as f:
        s3_client.upload_fileobj(f, dictionary['bucketName'], dictionary['destination_blob_name'])

def to_csv(fileName:str, data:list, fields:list)->None:
    """Takes a list object and creates a CSV file that will me located under the root of this project directory.
    
    Arguments
     fileName (str): String containing the final nambe on witch the data will be written.
     data (list): List of tuples that will be written in a CSV format
     fields (list): List that will contain the headers for the CSV file that will be written.
    
    Returns:
        None
    """
    import csv
    import os
    from pathlib import Path

    csv.register_dialect('dblquote',
                         delimiter=',',
                         lineterminator='\n',
                         quotechar='"',
                         quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)
  
    path = Path(f'{os.getcwd()}/{fileName}')

    with path.open('w', encoding='utf-8') as csvfile:
        csv_out = csv.writer(csvfile, dialect='dblquote')
        csv_out.writerow(fields)
        for tub in data:
            csv_out.writerow(tub)

def delete_processed_file(file_final_path:str)->None:
    """Deletes a file
    
    Arguments
     file_final_path (str): This is the string of the full path on which the file is placed.

    Returns
     None
    """
    import os

    os.remove(file_final_path)

            
