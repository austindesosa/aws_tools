# aws_tools
This repository contains Python useful to interact with AWS resources such as EC2 instances and S3 buckets.
There are also JSON files to store infomation, and .txt files  containing scripts intended for EC2 instances.

File   aws_local.py   contains Python code meant to quickly and conveniently interact with AWS resources. For example, it can quickly read from and write to a JSON file containing IAM credentials, and use those credentials to launch or connect to AWS resources such as EC2 instances or S3 buckets. 

File   fake_aws_accounts.json   is an example of a JSON file such as you would use with aws_local.py to get IAM credentials.
All the information in there is fake, because publishing real IAM credentials would be a security risk. But it shows the structure of the JSON files
you can use to store IAM credentials and other account information to fetch when needed.
I recommend that you write your own JSON file in the style of fake_aws_accounts.json and call it "aws_accounts.json". That is the default JSON filename for some of the functions in aws_local.py

File   aws_ec2.json   contains information about the default type of EC2 instance I have used when testing the code in this repository.
The default EC2 instance is an Amazon Linux 2 AMI, t2.micro instance type, the most common free-tier eligible instance type. This JSON file represents that information in a programmatically convenient way.
In your own project, you can change it to represent your preferred instance type.

File   setup_script.txt   is a set of Linux commands I have found convenient as a bootstrap script for EC2 instances. It was developed on the kind of EC2 instances described in aws_ec2.json
In the AWS management console, if you manually launch an EC2 instance, you can put the file setup_script.txt in the "User Data" field to use it as a startup script.
It updates the compute instance, installs python3, and installs pip, making it easier to use Python on your EC2 instance. 

File  get-pip.py  is the file to install pip on your machine. You have probably seen this file before if you have ever put pip on your computer. The file setup_script.txt contains a curl statement to fetch that file from the internet. I put it in this repository because I find it convenient to have.

File  basic_vpc_launch.py  will launch a VPC containing one EC2 instance. The code here was inspired by the article "How I Created And Configured An AWS VPC With Python" by Prateekh Singh ( https://blog.ipswitch.com/how-to-create-and-configure-an-aws-vpc-with-python ). 

