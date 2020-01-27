#!/bin/bash
. ~/.bash_profile
#################################################
#
#  This is the bash script that is being run by 
#  cron and runs DataEngineering-QueryRunner 
#  
#
#  Change History
#  --------------------------------
#  Luis Fuentes initial
#################################################

cd /ishome/ssg/lf188653/projects/DataEngineering-Query_Runner/
/ishome/ssg/lf188653/.conda/envs/testenv/bin/python main.py open_case_tracking_numbers
