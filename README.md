# AWS Lambda Setup in python 

This is the simple aws lambda setup. It contains a simple function which executes in aws lambada. It also has utitlies
to create zip file and upload it to aws lambda.


```bash
main.py - main file to be uploaded to executed in aws lambda
tools - uitlity scripts to upload, zip, update code in aws lambda.
data - temporary direcoty to hold data files.
tests - test functions to test aws lambda.
```


```bash
lambda function url: https://lexl6ptb3h.execute-api.us-west-2.amazonaws.com/default/steel_eye_data_extraction
s3 file url: https://s3-us-west-2.amazonaws.com/steel-eye-prepare-json/tmp/output.json
```