import sys
import logging
import pymysql
import json
import db_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(db_config.rds_host, user=db_config.name,
                           passwd=db_config.password, db=db_config.db_name, connect_timeout=5)
except:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def handler(event, context):
    """
    Flow of control begins from this function
    """
    
    # Post data comes as a Json-String in event['body']
    post = json.loads(event['body'])

    name = post['name']
    email = post['email']

    if (is_present(email)):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'User already present in database'
            })
        }

    user_id = insert_user(name, email)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Insert Succesful',
            'user_id': user_id
        })
    }


def is_present(email):
    """
    This function checks if the email is already present in the database or not 
    Returns: Boolean
    """

    result_set = []
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        conn.commit()
        cur.execute("select * from `user` where `email`='%s'" % (email))
        result_set = [row for row in cur]
    conn.commit()
    if result_set:
        return True
    else:
        return False


def insert_user(name, email):
    """
    This function inserts a new user and returns the new id 
    Returns: Integer
    """
    user_id = 0

    query = "insert into `user` (`name`, `email`) values('%s', '%s');" % (
        name, email)

    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        conn.commit()
        cur.execute(query)
        conn.commit()
        cur.execute("select last_insert_id()")
        user_id = cur.fetchone()['last_insert_id()']
    conn.commit()

    return user_id
