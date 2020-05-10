![deploy-to--lambda](https://github.com/jacknely/cmm_put_lambda/workflows/deploy-aws-lambda/badge.svg)
![Python application](https://github.com/jacknely/cmm_put_lambda/workflows/Python%20application/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
zip -r package.zip handler.py
```
Deploy to AWS:
```
serverless deploy
```
