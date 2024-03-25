#  ## Download the csv file from S3

# import boto3

# # Set up credentials for public S3 bucket 
# aws_access_key_id='X'
# aws_secret_access_key='X'
# bucket_name = 'waymark-assignment'
# object_key = 'outpatient_visits_file.csv'
# destination_folder = 'outpatient_visits_file.csv'

#  # Make S3 client with access keys
# s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

#  # Download the file to local folder
# s3.download_file(bucket_name, object_key, destination_folder)

import pandas as pd
import numpy as np
import calendar
import datetime as dt
import dateutil

## Read in the file

df = pd.read_csv('outpatient_visits_file.csv', 
                 usecols=['patient_id', 'date','outpatient_visit_count'],
                 parse_dates=['date'], 
                 encoding="utf-8-sig",
                 low_memory=False,
                 index_col=False)

# Drop all the blank rows
df_clean = df.dropna(how='all')

# Change float to integer
df_clean['outpatient_visit_count'] = df_clean['outpatient_visit_count'].astype(int)

# Double check for any remaining missing values
# print(df_clean.isna().sum())

## Read in the enrollment file
df_enrollment = pd.read_csv('patient_enrollment_span.csv', 
                            sep=',',
                 usecols=['patient_id', 'enrollment_start_date', 'enrollment_end_date'],
                 parse_dates=['enrollment_start_date', 'enrollment_end_date'], 
                 encoding="ISO-8859-1", 
                 low_memory=False
                )

# Join the two dfs together
df_joined = pd.merge(df_clean, df_enrollment)

# Check whether encounter date is between enrollment start and end dates
df_joined['in_enrollment_period'] = df_joined['date'].between(df_joined['enrollment_start_date'], df_joined['enrollment_end_date'])

df_joined['ct_days_with_outpatient_visit'] = df_joined.groupby(['patient_id'])['date'].transform('nunique')

#Rename columns
df_joined.columns = ['patient_id','encounter_date', 'ct_outpatient_visits', 'enrollment_start_date', 'enrollment_end_date', 'in_enrollment_period', 'ct_days_with_outpatient_visit']

#Reorder columns
df_final = df_joined.iloc[:,[0,3,4,2,6]]

#Save output file
df_final.to_csv('result.csv', encoding='utf-8', index=False)

#Get number of unique values in ct_days_with_outpatient_visit column
n = len(pd.unique(df_final['ct_days_with_outpatient_visit']))

print("Number of distinct values for ct_days_with_outpatient_visit ", n)