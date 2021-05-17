import json
import boto3
from datetime import datetime
def lambda_handler(event, context):
    
    print(event)
    print("hello")
    x=event
    s1=json.dumps(x)
    y=json.loads(s1)
    aws_region=y["region"]
    time=y["time"]
    print(aws_region)
    u_name=y["detail"]["userIdentity"]["userName"]
    print(u_name)
    instance_id=x["detail"]["responseElements"]["instancesSet"]["items"][0]["instanceId"]
    state=x["detail"]["responseElements"]["instancesSet"]["items"][0]["instanceState"]["name"]
    print(instance_id)
    print(state)
    start_time=y['time']
    print(start_time)
    ints=[]
    ints.append(instance_id)
    dynamodb =boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('cloudwatch_lambda')   
    dynamoTable.put_item(
        Item= {
             'InstanceId':instance_id,
             'UserName':u_name,
             'Region':aws_region,
             'StartTime':start_time,
             'TerminatedTime':""
            
    }
    )
    
    ec2 = boto3.client('ec2', region_name=aws_region)
    if((aws_region=="us-east-1") and (u_name=="Animesh")):
       print("inside if")
       ec2.terminate_instances(InstanceIds=ints)
       print('stopped your instances: ' + str(ints))
       now = datetime.now()
       date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
       print("date and time:",date_time)
       dynamoTable.update_item(
            Key={
            'InstanceId':instance_id
            },
            UpdateExpression='SET TerminatedTime = :val',
            ExpressionAttributeValues={
             ':val': date_time,
    },
            ReturnValues="UPDATED_NEW"
        )
       
    
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }
