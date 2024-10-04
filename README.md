# Part 1: Infrastructure Deployment Using Terraform
## Application: Cloud-based document processing.


I made  a cloud-based processing and review of documents application involving the use of multiple AWS services, along with Python automation. The system processes the uploaded document, be it an invoice, contract, or anything else, and saves the department-specific processed data in the cloud. For setting up the cloud infrastructure I have used a terraform script Here I took the Finance department which only deals with the amount to be paid, vendor’s account number and his name; every other information is secondary to it, the main focus lies on these 3 things.
With that, here is a breakdown of all the services used and their roles.


## Services used in the assignment with their roles.


<strong>Terraform (for Infrastructure-as-Code):</strong> 

This includes automating the deployment and management of AWS infrastructure, including S3 buckets, SQS queues, and EC2 instances, among other necessary resources.

How it's used:

Terraform will provide the cloud infrastructure, and everything from S3 to SQS, EC2, right down to Secrets Manager will be correctly implemented and will, consequently, maintain state management.


<strong>Amazon S3</strong> is a scalable, secure cloud storage service for storing and retrieving any amount of data. It’s perfect for managing files like documents, images, and videos, and integrates with other AWS services for easy data handling.

<strong>AWS Lambda</strong> is a serverless computing service that runs code without needing to manage servers. It automates tasks, scales automatically, and charges only for the compute time used, making it a cost-effective solution for backend operations.

<strong>AWS Transcribe</strong> converts spoken language into written text using advanced machine learning. It supports multiple languages and handles various audio qualities, making it ideal for transcribing audio and video content.

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