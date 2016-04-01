# SeekPanda_SmartMatch

## The primary objective
Provide suggestion of top matches to matchmakers.

### Work flow:
1. (Phase III)Check new jobs, record the job_id(s)
2. (Phase I)Update the extracted file by extracting the target fields in job file and pandas file.
3. (Phase II)For each new job, find top 3 candidates via smart match
4. (Phase III)Push the results to Slack

### Phase I: Data Engineering
1. Parse the job_details and price field to target fields
2. Data quality check:
  1) combine two deadline fields into one and change time period to time stamp
  2) Assign missing value for target price to 999999
3. Parse the target price from price field

### Phase II: Smart Match
1. For each job, check whether the location match
2. For each job, check the match_score for industry_weight and industry_performance
3. Calculate the match_percentage and return the top 3 candidate and their target price

### Phase III: Automation
1. Check the new job
2. Use phase I class, Extract the information and update the database
3. Use phase II class, Find the top candidates

## Current Issues:
1. Back end changed, data has already parsed
2. Formula modification, industry_weight is same to every pandas
3. Google doc's credential are needed for automation. 
