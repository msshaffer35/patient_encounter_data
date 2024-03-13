# ## Download the csv file from S3

# import boto3

# # Set up credentials for public S3 bucket 
# aws_access_key_id = 'X'
# aws_secret_access_key = 'X'
# bucket_name = 'waymark-assignment'
# object_key = 'patient_id_month_year.csv'
# destination_folder = 'patient_id_month_year.csv'

#  # Make S3 client with access keys
# s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

#  # Download the file to local folder
# s3.download_file(bucket_name, object_key, destination_folder) 

import pandas as pd
import numpy as np
import calendar

## Read in the file

df = pd.read_csv('patient_id_month_year.csv', 
                 usecols=['patient_id', 'month_year'] ,
                 parse_dates=['month_year'], 
                 encoding="ISO-8859-1", 
                 low_memory=False)

# Drop all the blank rows
df_clean = df.dropna(how='all')

# Double check for any remaining missing values
# print(df_clean.isna().sum())

# Find the earliest and latest date for each patient
group_df = df_clean.groupby(['patient_id'])
group_months_df = group_df.agg(enrollment_start_date=('month_year', np.min), month_end_date=('month_year', np.max)) 

# The maximum date shows the first day of the month, but coverage is for the whole month. Change the maximum date to the last day of month
group_months_df['enrollment_end_date'] = group_months_df['month_end_date'] + pd.DateOffset(months=1) + pd.DateOffset(days=-1)

final_df = group_months_df.drop('month_end_date', axis=1)

final_df.to_csv('patient_enrollment_span.csv', encoding='utf-8')

# Get number of rows in final file
print("Number of rows in final file is " + str(len(group_months_df.index)))