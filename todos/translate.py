import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
traductor = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    respuesta_trad = traductor.translate_text(Text=result['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=event['pathParameters']['language'])
    
    item = {
        'id': result['Item']['id'],
        'text': respuesta_trad.get('TranslatedText'),
        'checked': result['Item']['checked'],
        'createdAt': result['Item']['createdAt'],
        'updatedAt': result['Item']['updatedAt'],
    }
    
    # create a response
    response = {
        "statusCode": 200,
        #"body": json.dumps(respuesta_trad.get('TranslatedText'), cls=decimalencoder.DecimalEncoder)
        "body": json.dumps(item)
    }

    return response