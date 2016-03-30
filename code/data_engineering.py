#!/usr/bin/env python

import pandas as pd
import json


class Data_process(object):
    '''
    Process the raw data from csv file and extract interested
    fileds to corresponding column
    '''
    def __init__(self,
                 jobs_file='data/raw_data_jobs.csv',
                 pandas_file='data/raw_data_pandas.csv',
                 jobs='job_details',
                 pandas_price='prices',
                 field_code={'industry': 'dropdown_7603830',
                             'service_type': 'listimage_7603806_choice',
                             'industry_depth': 'list_6462400_choice',
                             'location': 'dropdown_9077980',
                             'prep_file_URL': 'fileupload_7219011',
                             'deadline': 'list_9048040_choice',
                             'deadline2': 'list_9080733_choice'},
                 price_code={'target_price': 'interpretation_target'}
                 ):
        self.jobs_file = jobs_file
        self.pandas_file = pandas_file
        self.jobs = jobs
        self.pandas_price = pandas_price
        self.field_code = field_code
        self.df_jobs, self.df_pandas = self.read_csv()

    def read_csv(self):
        return pd.read_csv(self.jobs_file), pd.read_csv(self.pandas_price)

    def valid_record(self):
        return 
