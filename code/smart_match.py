""" Perform smart match for jobs"""

import pandas as pd


class Smart_match(object):
    '''
    Find the top 3 condidate for the job
    '''
    def __init__(self,
                 job_id,
                 jobs_file='result/extracted_jobs.csv',
                 pandas_file='result/extracted_pandas.csv'
                 ):
        self.job_id = job_id
        self.jobs_file = jobs_file
        self.pandas_file = pandas_file
        self.df_jobs, self.df_pandas = self.read_csv()

    def read_csv(self):
        '''
        Read csv file to pandas dataframe
        '''
        return pd.read_csv(self.jobs_file), pd.read_csv(self.pandas_file)

    def location_match(self):
        '''
        For each job, check whether panda's location match
        '''
        loc = self.df_jobs[self.df_jobs['id'] == self.job_id]['location']
        self.df_pandas['location_match'] = self.df_pandas['basecity'].apply(
                                        lambda x: x == loc)

    def performance_score(self):
        '''
        Calculate the performance_score for all pandas on the job
        '''
        self.df_pandas['performance_score'] = self.df_pandas['id'].apply(
                        lambda x: self.check_score(
                            panda=self.df_pandas[self.df_pandas['id'] == x]
                            )
                            )

    def check_score(self,
                    panda,
                    metric={
                           'specialities': 1,
                           'capabilities': 0.5
                            },
                    other=0.1):
        '''
        Help function to determine the socre for each panda
        '''
        industry = self.df_jobs[self.df_jobs['id'] == self.job_id].iloc[0]
        for k, v in metric.iteritems():
            if industry in panda[k].iloc[0]:
                return v
        else:
            return other

    def match_percentage(self):
        '''
        Calculate match_percentage for each pandas on the job based on:
        match_percentage = match_location * performance_score
        '''
        self.df_jobs['match_percentage'] = self.df_jobs['location_match'] *\
                                           self.df_jobs['performance_score']

    def main(self):
        '''
        Return top 3 candidates for the job
        '''
        self.
