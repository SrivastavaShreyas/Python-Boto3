 # Boto3 - The AWS SDK for Python

Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Amazon S3, Amazon EC2, AWS Cost Explorer, AWS Lambda and many more services.

## Python Version

`Boto3` was deprecated for `Python2.7` and henceforth it is recommended for the developers to use latest versions of `Python` or pin the version of Boto3.

## Getting Started

Expecting to have a pre-setup of `Python Environment` over the local. Moving forward, make sure that if you are using `Python3.x` version, then you must have updated version of 

`pip` as well.

Use the following command to get pip:

`sudo apt-get install python3-pip`

**NOTE:** 

If you're running Python 2.7.9+ or Python 3.4+,
Congrats, you should already have pip installed.

Then the most crucial step is to install the latest version of Boto3 in the local. 

`python3 -m pip3 install boto3`

After the installation of Boto3, set up of AWS – Credentials is must.

`[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET_KEY`


To check the credentials in your terminal, do this:

`~/.aws/credentials`

Next step is to set up the region where you want to work. To know more about AWS-Regions, navigate [here](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/). 

For exploring the `Cost Explorer` using `AWS-Bot3` , the region will be `us-east-1` only.

So, set up the default region with `~/.aws/config`

‘[default]
region = us-east-1`

## Alternate Method to Access AWS – ARN user!!!

The alternate method to connect with any AWS Account is to create an `IAM role` for a user and then with the help of  `ARN Credentials` a `Session-Token` can be generated which can help us access the AWS with the help of `Python-boto3-sdk`

