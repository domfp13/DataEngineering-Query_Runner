# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes  

from __future__ import annotations
from typing import Optional

def open_case_tracking_numbers() -> str:
    '''
    This is the open_case_tracking_numbers query, this is to support AWS UPS project
    
    Parameters:
    None
     
    Returns:
    str: Query string

    '''
    query = '''
            WITH tzo as 
            (select distinct adr.zipcode, tzo.gmt_diff as UTC_OFFSET
            from DW.T_CLAR_ADDRESS adr, dw.t_Clar_Time_Zone tzo
            where adr.address2time_zone = tzo.objid)
            select F_INBOUND_WAYBILL, tzo.UTC_OFFSET, 'CLAR' as F_SOURCE
            from (
                SELECT CO.F_INBOUND_WAYBILL, CO.F_CASE_SITE_ZIP
                FROM DW.T_DM_CASES_OPEN co
                left join DW.T_UPS_MASTER ups
                on co.F_INBOUND_WAYBILL = UPS.TRACKINGNUMBER and ups.deliverydate is null
                where F_INBOUND_WAYBILL is not null
                and F_SVC_TYPE Not In ('PROJECT')
                and F_SVC_REGION Not In ('CORP','ITOT')
                and co.f_open_pr_count > 0
                and F_INBOUND_WAYBILL like '1Z%') waybill
            join tzo
            on waybill.F_CASE_SITE_ZIP = tzo.zipcode
            UNION ALL
            select DISTINCT(SHIP_TRACKING_NUMBER), -14400 as UTC_OFFSET, 'DIMS' as F_SOURCE 
            FROM DW.V_MSTR_ORDER_STATUS v 
            LEFT JOIN DW.T_UPS_MASTER UPS 
            on V.SHIP_TRACKING_NUMBER = UPS.TRACKINGNUMBER 
            where v.INVOICE_DATE = trunc(sysdate - 1)  
             and v. SHIP_TRACKING_NUMBER like '1Z%' and UPS.TRACKINGNUMBER is null
            '''
    return query