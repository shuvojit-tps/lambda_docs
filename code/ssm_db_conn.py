import json
import boto3
import pymysql

def lambda_handler(event, context):
    """
    This function fetches db details from SSM Parameter Store and connects to database
    Parameter path used here:
    /shuvojitRDS/host
    /shuvojitRDS/user
    /shuvojitRDS/password
    /shuvojitRDS/db_name
    """
    
    client = boto3.client('ssm')
    res = client.get_parameters_by_path(Path="/shuvojitRDS/")
    db_config = {}
    
    for param in res["Parameters"]:
        db_config[param['Name'].split('/')[-1]] = param['Value']
    
    print(format(db_config))
    # connect to RDS using SSM Parameters
    try:
        conn = pymysql.connect(db_config['host'], user=db_config['user'],passwd=db_config['password'], db=db_config['db_name'], connect_timeout=5)
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
    
    print("Successfully connected to DB")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
