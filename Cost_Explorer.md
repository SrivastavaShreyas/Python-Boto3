# Cost Explorer - Boto3 

AWS Boto3 provides multiple service access like for [Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
AWS Cost Explorer has an easy-to-use interface that lets you visualize, understand, and manage your AWS costs and usage over time. But with AWS Boto3 SDK, we will be using `Python Client` to connect to our AWS account services.

## Client

A low-level client representing AWS Cost Explorer Service

You can use the Cost Explorer API to programmatically query your cost and usage data. You can query for aggregated data such as total monthly costs or total daily usage. You can also query for `Granular-Data`. This might include the number of daily write operations for Amazon DynamoDB database tables in your production environment.

```python
import boto3 
client = boto3.client('ce') 

```

### Service Endpoint For AWS-Cost Explorer

The service endpoint for cost explorer is 

- https://ce.us-east-1.amazonaws.com

There are multiple [methods](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#client) which can be used by our client to fetch data from the cost explorer as per our reuqirements in `JSON` format. 

The granularities supported by the AWS Cost Explorer are :

```python
HOURLY | DAILY | MONTHLY
```

The method used here to fetch the data from the cost explorer is [get_cost_and_usage](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_and_usage).

All the required paramenters are passed into the method and upon successful completion of the code, we will get the [response](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_and_usage).


## Prerequisites 

- [awscli](https://aws.amazon.com/cli/)
- Configure AWS credentials for target account
  - run `aws configure`
- [Cost Explorer Enabled](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-enable.html)
- [Verfied Amazon SES Sender email](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html)
- To send to other addresses, you need to [move SES out of sandbox mode](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html).
