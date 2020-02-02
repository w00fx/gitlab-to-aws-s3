import git
import os
import shutil
import boto3
import json
from zipfile import ZipFile

def git_clone_zip(user, password, repo_url, file, repo):
    git.exec_command('clone', 'https://' + user + ':' + password + '@' + repo_url, cwd='/tmp/') # Command to make a Git Clone
    src = os.path.realpath('/tmp/' + repo + '/') # Taking the real path to directory
    shutil.make_archive('/tmp/' + file,'zip',src) # Creating the zip file

def upload_to_s3(file, repo, bucket):
    file_zip = file + '.zip' # Variable with zip file name
    s3 = boto3.resource('s3') # boto3 client instance
    bucket = s3.Bucket(bucket) # connecting to s3 bucket
    bucket.upload_file('/tmp/' + file_zip, repo + '/' + file_zip) # Uploading file to S3

def url_parse(url):
    url_slice = url.split('//') # Split string on // (from https://)
    return url_slice[1] # Returning the URI string



def lambda_handler(event, context):

    # Creating variables and adding the values in it
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    repo_bucket = os.environ['S3_BUCKET']
    file_name = event['repository']['name'] + '-' + event['project']['default_branch']
    repo_name = event['repository']['name']
    repo_git_url = event['repository']['git_http_url']
    print('Start Commit ID: ' + event['commits'][0]['id'])

    # Function to parse the URL
    url_git = url_parse(repo_git_url)
    print('URL Parsed')
    # Function to download the repo and zip the files from repo
    git_clone_zip(username, password, url_git, file_name, repo_name)
    print('Repository cloned and zipped!')

    # Function to upload all files to S3
    upload_to_s3(file_name, repo_name, repo_bucket)
    print('File uploaded!')

    # Function to delete the repo downloaded
    shutil.rmtree('/tmp/' + repo_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed successfully')
    }
