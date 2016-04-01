"""
This class will auto detect the new job,
and then find the top 3 candidates for it,
finally push it to slack channel
"""


from smart_match import Smart_match
from data_engineering import Data_engineering
import slackweb
from time import sleep


class Automation(object):
    '''
    automate the smart match process
    '''
    def __init__(self,
                 url='wwww.seekpanda.com/#/jobs/',
                 webhook='https://hooks.slack.com/services/T02TZ1FKK/B0VEPAFFH/\
                 ALkrk9HLNebUZAC0jDJFxJkE'):
        # self.raw_job = raw_job
        # self.raw_pandas = raw_pandas
        # self.extracted_job = extracted_job
        # self.extracted_pandas = extracted_pandas
        self.webhook = webhook
        self.url = url

    def detect_new_job(self):
        '''
        Compare raw_job and extracted_job to find new jobs
        return the new jobs id
        '''
        pass

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
        print top_candidates
        for i in range(len(top_candidates)):
            content += str(top_candidates[i]) + '(str(prices[i]))' + ', '
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
            data = Data_engineering()
            data.main()
            find_candidate = Smart_match()
            candidates, prices = find_candidate.main()
            content = self.content(job_id=2,
                                   top_candidates=candidates,
                                   prices=prices)
            self.push_to_slack(content=content)
            sleep(900.0)

if __name__ == '__main__':
    seek_panda = Automation()
    seek_panda.main()
