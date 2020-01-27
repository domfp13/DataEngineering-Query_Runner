# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes

from __future__ import annotations
from typing import Optional
import cx_Oracle

class OracleConnection():
    """This class returns a Oracle Connection"""

    def __init__(self):
        """This is the initalizer of the OracleConnection Class
        """
        self.server: str = "DW.WORLD"
        self.user_name: str = "SVCCAN_BCH"
        self.password: str = "B67YBCH"
        self.db_instance = cx_Oracle.connect(self.user_name, self.password, self.server)

    def sql_to_data(self, sqlText, dict_values: dict) -> list:
        """This method returns a list of tuples for a specific sql passover parameter, this one is for bindings. 

        Parameters:
            sqlText (str): The SQL query that will be execute.
            dict_values (dict): The dictionary that contains the values that will be bind.

        Returns:
            (list): result of the query execution.
        """
        result = []
        try:
            cursor = self.db_instance.cursor()
            rows = cursor.execute(sqlText, dict_values).fetchall()
            for row in rows:
                result.append(row)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            return result
    
    def sql_to_data_no_binding(self, sqlText) -> list:
        """This method returns a list of columns (query headers) and a list of tuples for a specific sql passover parameter (NO bidings).

        Parameters:
            sqlText (str): The SQL query that will be execute.

        Returns:
            (list): result of the query execution.
        """
        result = []
        col_names = []
        try:
            cursor = self.db_instance.cursor()
            rows = cursor.execute(sqlText).fetchall()
            for row in rows:
                result.append(row)
            
            col_names = [row[0] for row in cursor.description]
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            return col_names, result
    
    def __del__(self):
        self.db_instance.close()
