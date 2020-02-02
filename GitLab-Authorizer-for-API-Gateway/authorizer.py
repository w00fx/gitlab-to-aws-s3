from __future__ import print_function
import os
 
def generatePolicy(principalId, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = principalId
 
    if effect and methodArn:
        policyDocument = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': methodArn
                }
            ]
        }
 
        authResponse['policyDocument'] = policyDocument
 
    return authResponse
 
def lambda_handler(event, context):
    if event['authorizationToken'] == os.environ['API_KEY']:
        print('Request allowed')
        return generatePolicy(None, 'Allow', event['methodArn'])
 
    print('Request denied')
    return generatePolicy(None, 'Deny', event['methodArn'])
