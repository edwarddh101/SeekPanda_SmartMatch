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
                 prices='prices',
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
        self.prices = prices
        self.field_code = field_code
        self.df_jobs, self.df_pandas = self.read_csv()

    def read_csv(self):
        '''
        read csv file to pandas dataframe
        '''
        return pd.read_csv(self.jobs_file), pd.read_csv(self.pandas_price)

    def valid_record(self):
        '''
        Delete empty record and string to json object in job_details
        and pandas_file
        '''
        # jobs file
        self.df_jobs = self.df_jobs[pd.notnull(self.df_jobs[self.jobs])]
        self.df_jobs[self.jobs] = self.df_jobs[self.jobs].apply(
                                    lambda x: json.loads(x[11:-2]))
        # pandas file
        empty = {}
        start = '{"'
        self.df_pandas = self.df_pandas[self.df_pandas[self.prices] != empty]
        self.df_pandas[self.prices] = self.df_pandas[self.prices].apply(
                                    lambda x: json.loads(start+x[1:-1]))

    def extract_fields_jobs(self,
                            time_period={'In the next 24 hours': 1,
                                         'In the next week': 7,
                                         'Sometime later': 30},
                            deadline='deadline',
                            deadline2='deadline2',
                            inserted_at='inserted_at'
                            ):
        '''
        Extract target fields in jobs and pandas file
        '''
        # jobs file
        self.df_jobs[inserted_at] = pd.to_datetime(self.df_jobs[inserted_at])
        for k, v in self.field_code.iteritems():
            self.df_jobs[k] = self.df_jobs['job_details'].apply(lambda x: x[v])
        # Combine deadline information
        self.df_jobs[deadline].fillna(self.df_jobs[deadline2],
                                      inplace=True)
        del self.df_jobs[deadline2]
        self.df_jobs[deadline].str.strip()
        # change time period to time stamp
        self.df_jobs[deadline].replace(time_period, inplace=True)
        self.df_jobs[deadline] = pd.to_timedelta(
                                    self.df_jobs[deadline],
                                    unit='d') + self.df_jobs[inserted_at]
