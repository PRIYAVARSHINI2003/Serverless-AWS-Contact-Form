import json
import boto3

# Initialize the SNS client globally
sns = boto3.client('sns')

# Replace with the ARN of your SNS Topic (will create this in Step 4)
SNS_TOPIC_ARN = "arn:aws:sns:ap-southeast-2:565199753985:ContactFormSubmissions" 

def lambda_handler(event, context):
    try:
        # The form data comes in the 'body' of the API Gateway event
        if 'body' in event:
            data = json.loads(event['body'])
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid request format.'})
            }

        name = data.get('name', 'N/A')
        email = data.get('email', 'N/A')
        message = data.get('message', 'No message provided')

        # --- Prepare and Publish to SNS ---
        subject = f"New Contact Form Submission from {name}"
        body_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=body_message,
            Subject=subject
        )

        # --- Return success response to the website ---
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*', # CRUCIAL for CORS
            },
            'body': json.dumps({'message': 'Thank you! Your message has been sent.'})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'message': 'Failed to send message.'})
        }