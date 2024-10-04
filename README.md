# Part 1: Infrastructure Deployment Using Terraform
## Application: Cloud-based document processing.


I made  a cloud-based processing and review of documents application involving the use of multiple AWS services, along with Python automation. The system processes the uploaded document, be it an invoice, contract, or anything else, and saves the department-specific processed data in the cloud. For setting up the cloud infrastructure I have used a terraform script Here I took the Finance department which only deals with the amount to be paid, vendor’s account number and his name; every other information is secondary to it, the main focus lies on these 3 things.
With that, here is a breakdown of all the services used and their roles.


## Services used in the assignment with their roles.


<strong>Terraform (for Infrastructure-as-Code):</strong> 

This includes automating the deployment and management of AWS infrastructure, including S3 buckets, SQS queues, and EC2 instances, among other necessary resources.

How it's used:Terraform will provide the cloud infrastructure, and everything from S3 to SQS, EC2, right down to Secrets Manager will be correctly implemented and will, consequently, maintain state management.


<strong>Amazon S3: Simple Storage Service</strong>

Use the original documents (for example, PDFs) for uploading the invoice.

How it's used:

Files such as `SampleInvoice.pdf` would be stored in an S3 bucket, `myways-s3-bucket-2184`
It stores the department-raw processed data into the S3 bucket under particular folders, such as `processed/finance/`, right after processing.

If the Invoice is in your local desktop(not on the ec2 instance) then copy your file to the ec2 instance using the below command.

`scp -i /path/to/your/key_pair.pem "D:\SampleInvoice.pdf" ubuntu@<ec2-public-ip>:/home/ubuntu/`

Upload the pdf file from your ec2 instance to the s3 bucket using the below command.

`aws s3 cp /home/ubuntu/SampleInvoice.pdf s3://myways-s3-bucket-2184/`

For verification of the file use the below command.

`aws s3 ls s3://myways-s3-bucket-2184/`


<strong>Amazon SQS: Simple Queue Service</strong>

This queuing service decouples requests for document processing by storing messages that contain the information on which document to process and enabling asynchronous processing.

How it is used:

An SQS queue named `document-processing-queue_2184` is written to, with message details about which S3 bucket and file , in this case `SampleInvoice.pdf`.

The feature should be used when retrieving the message from the SQS queue and processing the document through an application or Python script; afterwards, the message should be deleted.

`aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/3240XXXXX890/document-processing-queue_2184 \ --message-body "{\"bucket_name\":\"myways-s3-bucket-2184\", \"file_key\":\"SampleInvoice.pdf\"}" --region us-east-1`

<strong>AWS Textract</strong> 

AWS Extract is used for the extraction of text, data, or metadata from documents, such as invoices and contracts.

How it is used:

The Python script, `document_processing.py`, processes the document recovered from S3 using AWS Textract for document processing.
The departmental output can be detected to be transformed into different form.

<strong>AWS Secrets Manager</strong> 

Secret Manager is used for storing and managing sensitive credentials like AWS API keys, database credentials, etc., needed by the application securely.

How it is used:

TThe Python script document_processing.py  needs access to AWS services (S3, SQS, Textract). Instead of embedding AWS Access Keys and Secret Keys into the script, Secrets Manager stores these credentials securely.The application retrieves the AWS credentials at runtime from Secrets Manager to authenticate API calls to various AWS services.

<strong>AWS EC2: Elastic Compute Cloud</strong> 

Ec2 does the document processing service on this host. The EC2 instance runs the Python script which automates the workflow, reading SQS messages, processing documents, and saving results.

How it is used:

The Ubuntu-based EC2 actually executes the script, called `document_processing.py`, that coordinates all of the work, including retrieving a document from S3, processing it using Textract, and saving results back to S3.

You SSH to an EC2 instance and run your commands in a managed environment.

`python3` and a virtual environment `myenv` is where all the necessary packages, including `boto3`, are to be installed in managing the environment.

## Command Execution

After the whole infrastructure of aws is set-up using the `main.tf` script, here are the commands that I have executed one-by-one for managing and using the services.

### ssh into the aws ec2 instance

`ssh -i myways_ec2_keypair.pem ubuntu@<public_ip_of_ubuntu_instance>`

### Install python3 and Pip

`sudo apt install python3 python3-pip`

### Set Up Python Virtual Environment

`python3 -m venv myenv`
`source myenv/bin/activate`

### Install the aws cli on the ec2 instance

`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`

##### Unzip the installer

`sudo apt-get install unzip -y`

#### Run the AWS CLI installer

`sudo ./aws/install`

###### Verify the Installation

`aws --version`


## Execution Flow & Results

* **The audio/video file is uploaded in the S3 bucket**
  ![S3bucket](Images/S3bucket.png)

* **AWS IAM: The role is executed here with 3 policies namely**
  * AccessS3ReadOnlyAccess
  * AmazonTranscribeFullAccess
  * CloudWatchFullAccess
  ![IAM](Images/IAM.png)

* **The purpose of the Lambda function is to initiate a transcription job using the Amazon Transcribe service when an audio or video file is uploaded to an S3 bucket.**
  ![Lambda](Images/lambdaa.png)

* **AWS Transcribe: Within the Transcription section of the project, the resulting text extracted from the audio/video file residing in the S3 bucket is displayed under the Transcription Preview section**
  ![Output](Images/ouput.png)