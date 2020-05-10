# :office: CMM Put: AWS Lambda Function
Python application that extracts cmm data from files uploaded to S3.
Extracted data is parsed and the uploaded to AWS DynamoDB

## Requirement
Install from requirements.txt:
- Python 3.6, 3.7, 3.8
- Requests

## Manual Deploy to Lambda
Ensure all required packages are install at root:
```
pip3 install requests -t .
```
Update application details in `serverless.yml`
Zip all files
```
zip -r package.zip *
```
Deploy to AWS:
```
serverless deploy
```
