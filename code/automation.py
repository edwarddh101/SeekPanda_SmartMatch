"""
This class will auto detect the new job,
and then find the top 3 candidates for it,
finally push it to slack channel
"""


from smart_match import Smart_match
from data_engineering import Data_engineering
import slackweb
from time import sleep
import pandas as pd


class Automation(object):
    '''
    automate the smart match process
    '''
    def __init__(self,
                 raw_jobs='data/raw_data_jobs.csv',
                 raw_pandas='data/raw_data_pandas.csv',
                 extracted_job='result/extracted_job.csv',
                 extracted_pandas='result/extracted_pandas.csv',
                 url='wwww.seekpanda.com/#/jobs/',
                 webhook='https://hooks.slack.com/services/T02TZ1FKK/B0VEPAFFH/\
                 ALkrk9HLNebUZAC0jDJFxJkE'):
        self.raw_jobs = raw_jobs
        self.raw_pandas = raw_pandas
        self.extracted_job = extracted_job
        self.extracted_pandas = extracted_pandas
        self.webhook = webhook
        self.url = url
        self.new_jobs = self.detect_new_job()

    def detect_new_job(self):
        '''
        Compare raw_job and extracted_job to find new jobs
        return the new jobs id
        '''
        df_raw_jobs = pd.read_csv(self.raw_jobs)
        df_extracted_job = pd.read.csv(self.extracted_job)
        return [i for i in df_raw_jobs['id'] if i not in df_extracted_job]

    def content(self,
                job_id,
                top_candidates,
                prices):
        '''
        generate the content based on smart match
        '''
        content = 'Hey guys! For job '
        content += self.url + str(job_id) + ', '
        content += 'please invite (in order) these people: '
        for i in range(len(top_candidates)):
            content += str(top_candidates.iloc[i]) +\
                       '($' + str(prices.iloc[i]) + ')' + ', '
        return content

    def push_to_slack(self, content):
        '''
        push the top candidates, price and job information to
        slack channel
        '''
        slack = slackweb.Slack(url=self.webhook)
        slack.notify(text=content)

    def main(self):
        '''
        automation the detection, smart match and push the result
        '''
        while True:
            for job in self.new_jobs():
                data = Data_engineering(raw_jobs=self.raw_jobs,
                                        raw_pandas=self.raw_pandas,
                                        extracted_jobs=self.extracted_jobs,
                                        extracted_pandas=self.extracted_pandas)
                data.main()
                find_candidate = Smart_match(job_id=job,
                                             jobs_file=self.extracted_jobs,
                                             pandas_file=self.extracted_pandas)
                candidates, prices = find_candidate.main()
                content = self.content(job_id=job,
                                       top_candidates=candidates,
                                       prices=prices)
                self.push_to_slack(content=content)
            sleep(900.0)

if __name__ == '__main__':
    seek_panda = Automation()
    seek_panda.main()
