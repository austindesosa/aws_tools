# -*- coding: utf-8 -*-
"""aws_local.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZWGzQ27MO2BSMKgVHnnwRqomSoIibbGs

This file is meant to use boto3 to connect with AWS resources on a local machine (as opposed to google colab).
"""

import os

INSTALL_BOTO = False #boolean whether you need to pip install boto3
#True if you need to install it, False if boto3 ois already pip installed
if INSTALL_BOTO:
  os.system('pip install boto3') 

WINDOWS_COMPAT = False #boolean whether you want to change Numpy version
#to be Windows compatible

if WINDOWS_COMPAT:
  os.system('pip uninstall numpy')
  os.system('pip install numpy==1.19.3')

import numpy as np
import pandas as pd


import json
import glob
from datetime import datetime
from time import time
import boto3



MAKE_REQS = True #Boolean telling whether you should make a requirements.txt file
REQS_NAME = 'aws_requirements.txt' #name of file containing requirements
if MAKE_REQS:
  os.system(f'pip freeze > {REQS_NAME}')

REGION = 'us-west-2'

def iam_credentials(csv_name = 'new_user_credentials.csv', dxry=None):
  '''Gets IAM credentials from a CSV file as provided by AWS for that purpose,
  returns tuple containing (username, dictionary of credentials)
  csv_name : string, name of CSV file
  dxry : Dictionary or NoneType, optional dictionary to add return value to
  Returns
  key : string, name of IAM user, 
  val : dictionary, contains access key ID and secret access key for that IAM user
  Also adds key-value pair (key, val) to dictionary dxry'''
  daf = pd.read_csv(csv_name)
  key = daf['User name'][0]
  val = {}
  val['access_key_id'] = daf['Access key ID'][0]
  val['secret_access_key'] = daf['Secret access key'][0]
  if dxry:
    dxry[key]=val
  return key, val

def quick_iam_dxry(json_file = 'aws_accounts.json', 
                   acct_name = 'austin_poyz',
                   key_name = 'iam_users'):
  '''Returns dictionary of IAM user credentials stored in a JSON file
  json_file : string, name of JSON file in your directory containing the needed information
  acct_name : string, name of AWS account to which IAM users belong
  key_name : string, dictionary key whose value is a dictionary containing IAM users and their credentials
  '''
  ret = json.load(open(json_file))[acct_name][key_name]
  return ret

def update_json(dxry,
                bucket, 
                your_fname='aws_accounts.json', 
                aws_fname='aws_accounts.json'):
  '''Updates the contents of a JSON file and uploads it to an S3 bucket
  dxry : dictionary, represents new contents of the JSON file
  bucket : boto3.resources.factory.s3.Bucket object representing S3 bucket to upload to
  your_fname : string, filename of JSON file in your present directory
  aws_fname : string, name you want the file to have in your s3 bucket
  Returns None
  '''
  with open(your_fname, 'w') as f:
    f.write(json.dumps(dxry))
  bucket.upload_file(your_fname, aws_fname)

def upload_to_dataset(df, 
                     your_fname, 
                     aws_fname, 
                     bucket,
                     y_label = 0, 
                     key_name='filename',
                     value_name='y_label'
                     ):
  '''Uploads file to bucket, gives it a label for machine learning,
  logs that information to a pandas.DataFrame
  df : pandas.DataFrame, to store the information along with info about other file-label pairs
  your_fname : string, name of file in your directory
  aws_fname : string, name of file it will have in bucket,
  y_label : int, category of image uploaded for neural network purposes
  bucket : boto3.resources.factory.s3.Bucket object for bucket to upload to
  key_name : string, column label storing filenames
  value_name : string, column label containing machine learning labels
  Returns dictionary whose values are the filename and the machine learning label'''
  bucket.upload_file(your_fname, aws_fname)
  dx = {key_name : aws_fname,
       value_name : y_label,
       }
  df.append(dx)
  return dx

def service(service_name, iam_name, iam_dxry, region='us-west-2', func = boto3.client):
  '''Returns an object mean to access an AWS service, as returned by boto3.resource or  boto3.client methods
  service_name : string, name of desired AWS service
  iam_name : string, name of IAM user whose credentials will be used to access the service,
  iam_dxry : dictionary, keys are IAM usernames and values are dictionaries containing IAM credentials,
  region : string , name of AWS region hosting the service,
  func : boto3.client | boto3.resource, Python function to connect to the service
  Returns object of the same type as returned by func
  '''
  creds = iam_dxry[iam_name]
  aki, sak = creds['access_key_id'], creds['secret_access_key']
  ret = func(service_name, 
             region_name = region,
             aws_access_key_id = aki,
             aws_secret_access_key = sak)
  return ret