import boto3
import json

s3_client = boto3.client('s3', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')
textract_client = boto3.client('textract', region_name='us-east-1')

queue_url = 'https://sqs.us-east-1.amazonaws.com/3240XXXXX4890/document-processing-queue_2184'
bucket_name = 'myways-s3-bucket-2184'

def retrieve_document_from_s3(bucket_name, file_key):
    """Retrieve the document from S3."""
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read()

def extract_text_from_document(document_bytes):
    """Extract text from the document using AWS Textract."""
    response = textract_client.detect_document_text(
        Document={'Bytes': document_bytes}
    )

    text_blocks = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_blocks.append(block['Text'])

    return text_blocks

def extract_finance_data(textract_response):
    """Extract finance-specific data: Vendor Name, Account Number, Total Amount."""
    finance_data = {
        'Vendor Name': None,
        'Account Number': None,
        'Total Amount': None
    }

    for line in textract_response:
        if 'Vendor Name' in line:
            finance_data['Vendor Name'] = line.split(':')[-1].strip()
        if 'Account Number' in line:
            finance_data['Account Number'] = line.split(':')[-1].strip()
        if 'Total Amount' in line or 'Amount Due' in line:
            finance_data['Total Amount'] = line.split(':')[-1].strip()

    return finance_data

def save_to_s3(bucket_name, file_key, data):
    """Save extracted data to S3."""
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(data))
    print(f"Data saved to {file_key}")

def process_document(queue_url):
    """Poll the SQS queue and process the document."""
    while True:
        response = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)

        if 'Messages' in response:
            for message in response['Messages']:
                body = json.loads(message['Body'])
                bucket_name = body['bucket_name']
                file_key = body['file_key']
                document = retrieve_document_from_s3(bucket_name, file_key)
                textract_response = extract_text_from_document(document)
                finance_data = extract_finance_data(textract_response)
                save_to_s3(bucket_name, f'processed/finance/finance_data.json', finance_data)
                sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
                print("Message processed and deleted from queue.")
        else:
            print("No messages in the queue.")
process_document(queue_url)