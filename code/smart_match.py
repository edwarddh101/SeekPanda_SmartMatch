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
                           'specialties': 1,
                           'capabilities': 0.5
                            },
                    other=0.1):
        '''
        Help function to determine the socre for each panda
        '''
        job = self.df_jobs[self.df_jobs['id'] == self.job_id]
        industry = job['industry'].iloc[0]
        for k, v in metric.iteritems():
            if industry in panda[k].iloc[0]:
                return v
        return other

    def match_percentage(self):
        '''
        Calculate match_percentage for each pandas on the job based on:
        match_percentage = match_location * performance_score
        '''
        location_score = self.df_pandas['location_match']
        performance_score = self.df_pandas['performance_score']
        self.df_pandas['match_percentage'] = location_score * performance_score

    def main(self):
        '''
        Return top 3 candidates for the job
        '''
        self.location_match()
        self.performance_score()
        self.match_percentage()
        sorted_pandas = self.df_pandas.sort(columns='match_percentage',
                                            axis=0,
                                            ascending=False)
        top_pandas = sorted_pandas[:3]
        return top_pandas['name'], top_pandas['target_price']

if __name__ == '__main__':
    find_candidate = Smart_match(job_id=2)
    print find_candidate.main()
